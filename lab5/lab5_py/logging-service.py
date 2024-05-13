from flask import Flask, jsonify, request
import hazelcast
import argparse
from time import sleep
from subprocess import Popen
from psutil import Process
from consul import Consul
from json import loads


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "Logging service that interacts with Hazelcast")
    parser.add_argument("-p", "--port", required = True, type = int, choices = [5001, 5002, 5003], help = "Logging service port")
    args = parser.parse_args()
    return args


def get_cfg(key):
    value = cfg.kv.get(key)[1]["Value"]
    return loads(value)


def start_hazelcast():
    # Start Hazelcast process
    cmd_p = Popen(get_cfg("hz-node")["binary"], creationflags = get_cfg("hz-node")["creationflags"])
    print(f"[!] cmd.exe PID: {cmd_p.pid}")
    sleep(1)

    # Get Hazelcast (Java) process handle
    parent = Process(cmd_p.pid)
    children = parent.children(recursive = True)  # [winconn.exe, java.exe]
    java_p = children[1]
    print(f"[!] java.exe PID: {java_p.pid}")
    return java_p


cfg = Consul()
app = Flask(__name__)
@app.route("/process_log", methods = ["GET", "POST"])
def process_log():
    print(f"\n\n==== [REQ] {request.method} from facade-service")
    dmap = app.config["dmap"]
    if request.method == "POST":
        data = request.get_json()
        uuid = list(data.keys())[0]
        msg = data[uuid]
        print(f"Message: {msg}")
        print(f"UUID: {uuid}")

        dmap.put(uuid, msg)
        return jsonify({uuid: msg})

    elif request.method == "GET":
        msgs = dict(dmap.entry_set())
        return jsonify(msgs)

    else:
        return jsonify({"Error": "Unsupported request method"})


def main():
    args = parse_cli_args()
    port = args.port
    java_p = start_hazelcast()
    client = hazelcast.HazelcastClient(cluster_name = get_cfg("hz")["cluster_name"])

    cfg.agent.service.register(
        name = "logging-service",
        service_id = f"logging-service:{port}",
        address = "127.0.0.1",
        port = port
    )

    dmap = client.get_map(get_cfg("dmap")).blocking()
    app.config["dmap"] = dmap
    app.run(port = port)

    client.shutdown()
    java_p.terminate()


if __name__ == "__main__":
    # sys.argv = ["logging-service", "-p", "5001"]
    main()
