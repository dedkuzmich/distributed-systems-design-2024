import hazelcast


def msg_listener(msg):
    print(f"{msg.message} was read")


def main():
    client = hazelcast.HazelcastClient(cluster_name = "sam")

    topic_name = "topic_lab2"
    topic = client.get_topic(topic_name).blocking()
    listener = topic.add_listener(msg_listener)
    input("\n[!] Press Enter to stop listening...\n")
    topic.remove_listener(str(listener))

    client.shutdown()


if __name__ == "__main__":
    main()
