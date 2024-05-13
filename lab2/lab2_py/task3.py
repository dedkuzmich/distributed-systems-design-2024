import hazelcast


def main():
    client = hazelcast.HazelcastClient(cluster_name = "sam")

    dmap_name = "dmap_lab2"
    dmap = client.get_map(dmap_name).blocking()
    for key in range(1000):
        value = f"value_{key}"
        dmap.put(key, value)
    print(f"\n[+] {dmap_name} was filled\n")

    client.shutdown()


if __name__ == "__main__":
    main()
