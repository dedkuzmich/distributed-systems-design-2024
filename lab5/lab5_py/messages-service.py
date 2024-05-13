from flask import Flask, jsonify, request
import argparse
import hazelcast
import threading
from consul import Consul
from json import loads


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "Messaging service that interacts with Hazelcast")
    parser.add_argument("-p", "--port", required = True, type = int, choices = [6001, 6002], help = "Messaging service port")
    args = parser.parse_args()
    return args


def get_cfg(key):
    value = cfg.kv.get(key)[1]["Value"]
    return loads(value)


def queue_listener(queue, msgs):
    while True:
        msg = queue.take()
        msgs.append(msg)
        print(f"{msg} was taken")


cfg = Consul()
app = Flask(__name__)
@app.route(f"/process_msg", methods = ["GET"])
def process_msg():
    print(f"\n\n==== [REQ] {request.method} from facade-service")
    msgs = app.config["msgs"]
    if request.method == "GET":
        print("Messages list:", msgs)
        return jsonify({"Messages": msgs})

    else:
        return jsonify({"Error": "Unsupported request method"})


def main():
    args = parse_cli_args()
    port = args.port
    client = hazelcast.HazelcastClient(cluster_name = get_cfg("hz")["cluster_name"])

    cfg.agent.service.register(
        name = "messages-service",
        service_id = f"messages-service:{port}",
        address = "127.0.0.1",
        port = port
    )

    msgs = []
    queue = client.get_queue(get_cfg("queue")).blocking()
    listener_t = threading.Thread(target = queue_listener, args = [queue, msgs])
    listener_t.daemon = True  # Daemons are killed when the main program exits
    listener_t.start()

    app.config["msgs"] = msgs
    app.run(port = port)

    client.shutdown()


if __name__ == "__main__":
    # sys.argv = ["messages-service", "-p", "6001"]
    main()
