from consul import Consul
from subprocess import CREATE_NEW_CONSOLE
from json import dumps


def main():
    cfg = Consul()
    cfg.kv.put("queue", dumps("queue_lab5"))
    cfg.kv.put("dmap", dumps("dmap_lab5"))

    config = {
        "cluster_name": "sam"
    }
    cfg.kv.put("hz", dumps(config))

    config = {
        "binary": "hz-start.bat",
        "creationflags": CREATE_NEW_CONSOLE
    }
    cfg.kv.put("hz-node", dumps(config))


if __name__ == "__main__":
    main()
