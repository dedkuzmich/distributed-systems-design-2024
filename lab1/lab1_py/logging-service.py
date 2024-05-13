from flask import Flask, jsonify, request
import argparse


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "Logging service that interacts with Hazelcast")
    parser.add_argument("-p", "--port", required = True, type = int, choices = [5001, 5002, 5003], help = "Logging service port")
    args = parser.parse_args()
    return args


app = Flask(__name__)
@app.route("/process_log", methods = ["GET", "POST"])
def process_log():
    print(f"\n\n==== [REQ] {request.method} from facade-service")
    hash_tab = app.config["hash_tab"]
    if request.method == "POST":
        data = request.get_json()
        uuid = list(data.keys())[0]
        msg = data[uuid]
        print(f"Message: {msg}")
        print(f"UUID: {uuid}")

        hash_tab[uuid] = msg
        return jsonify({uuid: msg})

    elif request.method == "GET":
        msgs = hash_tab
        return jsonify(msgs)

    else:
        return jsonify({"Error": "Unsupported request method"})


def main():
    args = parse_cli_args()
    port = args.port

    hash_tab = {}
    app.config["hash_tab"] = hash_tab
    app.run(port = port)



if __name__ == "__main__":
    # sys.argv = ["logging-service", "-p", "5001"]
    main()
