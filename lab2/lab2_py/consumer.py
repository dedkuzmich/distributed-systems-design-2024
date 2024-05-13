import hazelcast


def main():
    client = hazelcast.HazelcastClient(cluster_name = "sam")

    queue_name = "default"
    queue = client.get_queue(queue_name).blocking()
    for i in range(50):
        value = queue.take()
        print(f"{value} was taken")

    client.shutdown()


if __name__ == "__main__":
    main()
