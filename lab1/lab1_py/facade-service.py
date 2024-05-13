from flask import Flask, request, jsonify
import argparse
from uuid import uuid4
import requests
from json import dumps


host = "http://127.0.0.1"
log_port = 5001
msg_port = 6001


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "Facade service that interacts with Client, Logging service & Messaging service")
    parser.add_argument("-p", "--port", required = True, type = int, choices = [4001], help = "Facade service port")
    args = parser.parse_args()
    return args


app = Flask(__name__)
@app.route(f"/process_req", methods = ["GET", "POST"])
def process_req():
    print(f"\n\n==== [REQ] {request.method} from client")

    if request.method == "POST":
        msg = request.get_data().decode()
        uuid = str(uuid4())
        print(f"Message: {msg}")
        print(f"UUID: {uuid}")

        # Interact with logging-service
        data = {uuid: msg}
        log_res = requests.post(f"{host}:{log_port}/process_log", json = data).json()
        print(f"  == [RES] from logging-service:{log_port}")
        print(dumps(log_res, indent = 4))

        res = jsonify({
            "logging-service": dict(log_res)
        })
        return res

    elif request.method == "GET":
        # Interact with logging-service
        log_res = requests.get(f"{host}:{log_port}/process_log").json()
        print(f"  == [RES] from logging-service:{log_port}")
        print(dumps(log_res, indent = 4))

        # Interact with messages-service
        msg_res = requests.get(f"{host}:{msg_port}/process_msg").json()
        print(f"  == [RES] from messages-service:{msg_port}")
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
    app.run(port = port)


if __name__ == "__main__":
    # sys.argv = ["facade-service", "-p", "4001"]
    main()
