import requests
from json import dumps


host = "http://127.0.0.1"
master_port = 4001


def post_request(msg, w):
    print("\n\n==== [REQ] POST to master")
    print(f"Write concern level: {w}")
    print(f"Message: {msg}")
    try:
        master_res = requests.post(f"{host}:{master_port}/process_req", json = {"w": w, "msg": msg}).json()
        print("  == [RES] from master")
        print(dumps(master_res, indent = 4))
    except Exception as e:
        print(f"[-] Master is unreachable")


def get_request():
    print("\n\n==== [REQ] GET to master")
    try:
        master_res = requests.get(f"{host}:{master_port}/process_req").json()
        print("  == [RES] from master")
        print(dumps(master_res, indent = 4))
    except Exception as e:
        print(f"[-] Master is unreachable")


def main():
    print("Client2 is running...")
    post_request("msg4", 1)
    post_request("msg5", 2)
    get_request()


if __name__ == "__main__":
    main()
