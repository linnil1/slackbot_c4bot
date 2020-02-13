from flask import Flask, request
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


@app.route("/command", methods=["POST"])
def command():
    data = dict(request.form)
    print(data)
    if not data.get('text'):
        return "Not text"
    # save to queue
    data["type"] = "command"
    name = data['trigger_id']
    json.dump(data, open(f"queue/{name}.json", "w"))
    return ""


# run
os.makedirs("queue", exist_ok=True)
os.makedirs("queue_fail", exist_ok=True)
app.run(host="0.0.0.0",
        port=configuration.web_port,
        ssl_context=configuration.ssl_context,
        debug=True)
