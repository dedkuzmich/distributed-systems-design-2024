from flask import Flask, request, jsonify
import argparse
from uuid import uuid4
import requests
from random import choice
from json import dumps, loads
import hazelcast
from consul import Consul


class Endpoint:
    def __init__(self, ip, port, url):
        self.ip = ip
        self.port = port
        self.url = url


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "Facade service that interacts with Client, Logging service & Messaging service")
    parser.add_argument("-p", "--port", required = True, type = int, choices = [4001], help = "Facade service port")
    args = parser.parse_args()
    return args


def get_cfg(key):
    value = cfg.kv.get(key)[1]["Value"]
    return loads(value)


def get_endpoints(service_name):
    endpoints = []
    services = cfg.health.service(service_name)[1]
    for service in services:
        ip = service["Service"]["Address"]
        port = service["Service"]["Port"]
        url = f"http://{ip}:{port}"
        endpoint = Endpoint(ip, port, url)
        endpoints.append(endpoint)
    return endpoints


cfg = Consul()
app = Flask(__name__)
@app.route(f"/process_req", methods = ["GET", "POST"])
def process_req():
    print(f"\n\n==== [REQ] {request.method} from client")
    queue = app.config["queue"]

    # Find 1 alive logging-service
    log_endpoints = get_endpoints("logging-service")
    if not log_endpoints:
        return jsonify({"Error": "logging-service is unavailable"})
    log_endpoint = choice(log_endpoints)

    # Find 1 alive messages-service
    msg_endpoints = get_endpoints("messages-service")
    if not msg_endpoints:
        return jsonify({"Error": "messages-service is unavailable"})
    msg_endpoint = choice(msg_endpoints)

    if request.method == "POST":
        msg = request.get_data().decode()
        uuid = str(uuid4())
        print(f"Message: {msg}")
        print(f"UUID: {uuid}")

        # Interact with logging-service
        data = {uuid: msg}
        log_res = requests.post(f"{log_endpoint.url}/process_log", json = data).json()
        print(f"  == [RES] from logging-service:{log_endpoint.port}")
        print(dumps(log_res, indent = 4))

        # Interact with messages-service
        queue.put(msg)

        res = jsonify({
            "logging-service": dict(log_res)
        })
        return res

    elif request.method == "GET":
        # Interact with logging-service
        log_res = requests.get(f"{log_endpoint.url}/process_log").json()
        print(f"  == [RES] from logging-service:{log_endpoint.port}")
        print(dumps(log_res, indent = 4))

        # Interact with messages-service
        msg_res = requests.get(f"{msg_endpoint.url}/process_msg").json()
        print(f"  == [RES] from messages-service:{msg_endpoint.port}")
        print(dumps(msg_res, indent = 4))

        res = jsonify({
            "logging-service": dict(log_res),
            "messages-service": dict(msg_res)
        })
        return res

    else:
        return jsonify({"Error": "Unsupported request method"})


def main():
    args = parse_cli_args()
    port = args.port
    client = hazelcast.HazelcastClient(cluster_name = get_cfg("hz")["cluster_name"])

    cfg.agent.service.register(
        name = "facade-service",
        service_id = f"facade-service:{port}",
        address = "127.0.0.1",
        port = port
    )

    queue = client.get_queue(get_cfg("queue")).blocking()
    app.config["queue"] = queue
    app.run(port = port)

    client.shutdown()


if __name__ == "__main__":
    # sys.argv = ["facade-service", "-p", "4001"]
    main()
