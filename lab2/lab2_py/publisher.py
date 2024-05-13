import hazelcast


def main():
    client = hazelcast.HazelcastClient(cluster_name = "sam")

    topic_name = "topic_lab2"
    topic = client.get_topic(topic_name).blocking()
    for value in range(1, 101):
        topic.publish(value)
        print(f"{value} was published")

    client.shutdown()


if __name__ == "__main__":
    main()
