from flask import Flask, request, jsonify
import logging
import argparse
from json import dumps


def setup_logger():
    stream_handler = logging.StreamHandler()
    stream_format = logging.Formatter("%(message)s")
    stream_handler.setFormatter(stream_format)

    file_handler = logging.FileHandler("service.log", mode = "w")
    file_format = logging.Formatter("%(asctime)s\t\t[%(levelname)s]\t\t%(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_format)

    logging.basicConfig(
        level = logging.INFO,
        handlers = [file_handler, stream_handler]
    )


def parse_cli_args():
    parser = argparse.ArgumentParser(description = "Secondary service")
    parser.add_argument("-p", "--port", required = True, type = int, help = "Secondary service port")
    args = parser.parse_args()
    return args


def track_new_entries(list1, list2):
    # Get entries that are present in list2 and not present in list1
    diff = []
    if len(list1) == len(list2):
        return diff
    if len(list1) > len(list2):  # Swap lists
        list1, list2 = list2, list1
    for entry in list2:
        if entry not in list1:
            diff.append(entry)
    return diff


setup_logger()
log = logging.getLogger(__name__)
app = Flask(__name__)
@app.route("/process_msg", methods = ["GET", "POST"])
def process_log():
    log.warning(f"\n\n==== [REQ] {request.method} from master")
    msg_list = app.config["msg_list"]
    if request.method == "POST":
        data = request.get_json()

        new_entries = track_new_entries(msg_list, data)  # Deduplication
        msg_list.extend(new_entries)
        msg_list.sort(key = lambda x: x["time"])  # Sort by time

        log.info("New messages:")
        log.info(dumps(new_entries, indent = 4))
        return jsonify(new_entries)

    elif request.method == "GET":
        return jsonify(msg_list)

    else:
        return jsonify({"Error": "Unsupported request method"})


def main():
    args = parse_cli_args()
    port = args.port

    app.config["msg_list"] = []
    app.run(host = "0.0.0.0", port = port)


if __name__ == "__main__":
    # sys.argv = ["secondary", "-p", "5001"]
    main()
