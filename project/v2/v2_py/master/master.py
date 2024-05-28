from flask import Flask, request, jsonify
import logging
import argparse
import requests
from os import environ
from urllib.parse import urlparse
from json import dumps
from uuid import uuid4
from datetime import datetime
from time import sleep


class Service:
    def __init__(self, hostname, port, url):
        self.hostname = hostname
        self.port = port
        self.url = url


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
    parser = argparse.ArgumentParser(description = "Master service")
    parser.add_argument("-p", "--port", required = True, type = int, help = "Master service port")
    args = parser.parse_args()
    return args


def gen_timestamp():
    now = datetime.now()
    fmt_now = now.strftime("%Y-%m-%d %H:%M:%S %f")
    fmt_now = fmt_now[:-3] + "." + fmt_now[-3:]  # Delimiter milliseconds and microseconds with "."
    return fmt_now


def get_services(env_var_urls):
    urls = environ.get(env_var_urls).split(",")
    services = []
    for url in urls:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        port = parsed_url.port
        service = Service(hostname, port, url)
        services.append(service)
    return services


setup_logger()
log = logging.getLogger(__name__)
app = Flask(__name__)
@app.route(f"/process_req", methods = ["GET", "POST"])
def process_req():
    log.warning(f"\n\n==== [REQ] {request.method} from client")
    msg_list = app.config["msg_list"]
    secondaries = app.config["secondaries"]

    if request.method == "POST":
        data = request.get_json()
        w = data["w"]
        msg = data["msg"]
        uuid = str(uuid4())
        time = gen_timestamp()

        log.warning(f"Write concern level: {w}")
        log.info(f"Message: {msg}")
        log.info(f"UUID: {uuid}")
        log.info(f"Timestamp: {time}")

        entry = {"msg": msg, "uuid": uuid, "time": time}
        msg_list.append(entry)
        res = {}
        res["master"] = entry

        # Interact with secondaries
        for secondary in secondaries:
            try:
                # Send message
                sec_res = requests.post(f"{secondary.url}/process_msg", json = entry).json()
                log.info(f"  == [RES] from {secondary.hostname}")
                log.info(dumps(sec_res, indent = 4))
                res[secondary.hostname] = sec_res
            except Exception as e:
                continue
        if len(res) >= w:  # Check the level of acknowledgement that the write concern requires
            return jsonify(res)
        else:
            error = f"Cannot satisfy write concern level = {w}"
            log.warning(error)
            return jsonify({"Error": error})

    elif request.method == "GET":
        # Interact with secondaries
        res = []
        for secondary in secondaries:
            try:
                sec_res = requests.get(f"{secondary.url}/process_msg").json()
                log.info(f"  == [RES] from {secondary.hostname}")
                log.info(dumps(sec_res, indent = 4))
                res.extend(sec_res)
            except Exception as e:
                continue
        if not res:
            log.warning("[-] No alive secondaries. Sending local in-memory list...")
            return msg_list

        res = list({v["uuid"]: v for v in res}.values())  # Deduplication
        res.sort(key = lambda x: x["time"])  # Sort by time
        return jsonify(res)

    else:
        return jsonify({"Error": "Unsupported request method"})


def main():
    args = parse_cli_args()
    port = args.port

    app.config["secondaries"] = get_services("SECONDARY_URLS")
    app.config["msg_list"] = []
    app.run(host = "0.0.0.0", port = port, threaded = True)  # Use threaded to serve multiple clients


if __name__ == "__main__":
    # sys.argv = ["master", "-p", "4001"]
    main()
