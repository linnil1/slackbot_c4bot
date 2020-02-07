from flask import Flask
from pprint import pprint
from slackeventsapi import SlackEventAdapter
import json
import os

import configuration


app = Flask(__name__)
sercet = configuration.signing_secret
events = SlackEventAdapter(sercet, "/slack", app)


# Create an event listener for "reaction_added" events and print the emoji name
@events.on("reaction_added")
def reaction_added(data):
    """Do nothing"""
    pprint(data)


@events.on("message")
def message(data):
    """Record all the message to queue"""
    print("Get message")
    pprint(data)
    message = data["event"]
    if not message:
        return "OK"
    name = message["ts"]
    json.dump(message, open(f"queue/{name}.json", "w"))
    return "OK"


# run
os.makedirs("queue", exist_ok=True)
os.makedirs("queue_fail", exist_ok=True)
app.run(host="0.0.0.0",
        port=12121,
        ssl_context=('data/fullchain.pem', 'data/privkey.pem'),
        debug=True)
