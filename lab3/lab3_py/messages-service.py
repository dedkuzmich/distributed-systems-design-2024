from flask import Flask, jsonify, request
import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "Messaging service that interacts with Hazelcast")
    parser.add_argument("-p", "--port", required = True, type = int, choices = [6001, 6002], help = "Messaging service port")
    args = parser.parse_args()
    return args


app = Flask(__name__)
@app.route(f"/process_msg", methods = ["GET"])
def process_msg():
    print(f"\n\n==== [REQ] {request.method} from facade-service")
    if request.method == "GET":
        return jsonify({"Stub": "Work in progress"})

    else:
        return jsonify({"Error": "Unsupported request method"})


def main():
    args = parse_cli_args()
    port = args.port
    app.run(port = port)


if __name__ == "__main__":
    # sys.argv = ["messages-service", "-p", "6001"]
    main()
