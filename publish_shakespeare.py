#!/usr/bin/env python
"""Simple example script demonstrating reading from GCS and writing to pub/sub."""

import json
import os
import re
import sys

# Imports the Google Cloud client library
from google.cloud import storage

# Imports the Google Cloud Pub/Sub library
from google.cloud import pubsub

def extract_play_spoken_lines(play_text):
    """Given a complete play text, extract the spoken lines."""

    spoken_pattern = re.compile(r"(?P<who>^(\w+ *)+)?(?:\t)?(?P<what>.*)")

    lines = []
    accum = {}
    play_lines = play_text.splitlines()
    spoken_lines_start = 0
    for line_number, line in enumerate(play_lines):
        if line.startswith("SCENE I"):
            spoken_lines_start = line_number+1
            break

    spoken_lines = play_lines[spoken_lines_start:]
    for line in spoken_lines:
        # blank
        if re.match(r"^$", line):
            continue
        # stage direction
        if re.match(r"^\s+\[", line):
            continue

        match = spoken_pattern.match(line)
        groups = match.groupdict()
        if groups["who"] is not None:
            lines.append(accum)
            accum = {"who":groups["who"], "said":[groups["what"]]}
        else:
            accum.setdefault("said", [])
            accum["said"].append(groups["what"])

    return [line for line in lines if line]


def publish_shakespeare(topic, lines):
    """Publish Shakespeare lines to pub/sub."""

    if not topic.exists():
        topic.create()

    for line in lines:
        topic.publish(json.dumps(line).encode('utf-8'))


def main():
    """Main function."""

    # Path to your service account keyfile
    service_account_keyfile = os.path.join(os.environ["HOME"], "serviceaccount.json")

    # Instantiates a storage client
    storage_client = storage.Client()

    # The name of the bucket
    shakespeare_bucket = "apache-beam-samples"

    # Object path - note lack of leading '/'
    object_path = "shakespeare/kinglear.txt"

    # Instantiates a pubsub client using a service account keyfile, if available.
    if os.path.exists(service_account_keyfile):
        pubsub_client = pubsub.Client.from_service_account_json(service_account_keyfile)
    else:
        pubsub_client = pubsub.Client()

    # Get a pub/sub topic. Setting timestamp_messages = True adds
    # a timestamp attribute when the message is accepted.
    topic = pubsub_client.topic("kinglear", timestamp_messages=True)


    bucket = storage_client.get_bucket(shakespeare_bucket)
    if not bucket:
        print >>sys.stderr, "Oops, no such bucket: ", shakespeare_bucket
        sys.exit(1)

    play_obj = bucket.get_blob(object_path)
    if play_obj:
        play = play_obj.download_as_string()
        spoken_lines = extract_play_spoken_lines(play)
        publish_shakespeare(topic, spoken_lines)

if __name__ == "__main__":
    main()
