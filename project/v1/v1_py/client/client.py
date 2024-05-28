import requests
from json import dumps


host = "http://127.0.0.1"
master_port = 4001


def post_request(msg):
    print("\n\n==== [REQ] POST to master")
    print(f"Message: {msg}")
    try:
        master_res = requests.post(f"{host}:{master_port}/process_req", json = {"msg": msg}).json()
        print("  == [RES] from master")
        print(dumps(master_res, indent = 4))
    except Exception as e:
        print(f"[-] Master is unavailable")


def get_request():
    print("\n\n==== [REQ] GET to master")
    try:
        master_res = requests.get(f"{host}:{master_port}/process_req").json()
        print("  == [RES] from master")
        print(dumps(master_res, indent = 4))
    except Exception as e:
        print(f"[-] Master is unavailable")


def main():
    print("Client is running...")
    post_request("msg1")
    post_request("msg2")
    post_request("msg3")
    get_request()

    print("\n\n------------------------------------")
    input("Stop one secondary and press Enter: ")

    post_request("msg4")


if __name__ == "__main__":
    main()
