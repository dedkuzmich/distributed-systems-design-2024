import requests
from json import dumps

host = "http://127.0.0.1"
facade_port = 4001


def post_request(data):
    print("\n\n==== [REQ] POST to facade-service")
    facade_res = requests.post(f"{host}:{facade_port}/process_req", data = data).json()
    print("  == [RES] from facade-service")
    print(dumps(facade_res, indent = 4))


def get_request():
    print("\n\n==== [REQ] GET to facade-service")
    facade_res = requests.get(f"{host}:{facade_port}/process_req").json()
    print("  == [RES] from facade-service")
    print(dumps(facade_res, indent = 4))


def main():
    print("Client is running...")

    for i in range(3):
        post_request(f"msg{i + 1}")
    get_request()


if __name__ == "__main__":
    main()
