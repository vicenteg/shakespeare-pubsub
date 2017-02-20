#!/usr/bin/env python
"""Simple example script demonstrating subscribing to a pub/sub topic."""

import json
import os

# Imports the Google Cloud Pub/Sub library
from google.cloud import pubsub


def pull_from(topic):
    """Subscribe to topic and pull lines from pub/sub."""

    if not topic.exists():
        topic.create()

    subscription = topic.subscription("my-subscription")
    if not subscription.exists():
        subscription.create()

    processed = []
    pulled = subscription.pull(max_messages=10)
    for (ack_id, message) in pulled:
        processed.append(ack_id)
        print "{who}   {said}".format(**json.loads(message.data))

    subscription.acknowledge(processed)


def main():
    """Main function."""

    # Path to your service account keyfile
    service_account_keyfile = os.path.join(os.environ["HOME"], "serviceaccount.json")

    # Instantiates a pubsub client using a service account keyfile, if available.
    if os.path.exists(service_account_keyfile):
        pubsub_client = pubsub.Client.from_service_account_json(service_account_keyfile)
    else:
        pubsub_client = pubsub.Client()

    # Get a pub/sub topic. Setting timestamp_messages = True adds
    # a timestamp attribute when the message is accepted.
    topic = pubsub_client.topic("kinglear", timestamp_messages=True)
    pull_from(topic)


if __name__ == "__main__":
    main()
