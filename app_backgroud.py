from pprint import pprint
import slack
import json
import os
import time
import re

import configuration
import sticker

token = configuration.token
client = slack.WebClient(token=token)


def echo(message):
    """Echo to person who call c4bot"""
    rep = {
        'channel': message["channel"],
        'text': f"Hello <@{message['user']}>!",
    }
    if message.get("thread_ts"):
        rep['thread_ts'] = message['thread_ts']

    response = client.chat_postMessage(**rep)
    pprint(response['message'])
    print("Response Done")


def responseSticker(message):
    """Google Search a image"""
    keyword = message.get("text")
    url = sticker.imageSearch(keyword)
    blocks = sticker.imageBlock(keyword, url)

    response = client.chat_postMessage(
                   channel=message["channel"],
                   blocks=blocks)
    pprint(response["message"])
    print("Response Done")


# main funciton
while True:
    # read from queue
    messages = os.listdir("queue")
    if not messages:
        time.sleep(1)
        continue
    name = "queue/" + messages[0]
    message = json.load(open(name))
    pprint(message)
    print(name)

    # run each module
    try:
        if not message.get("subtype") and not message.get("bot_id") and not message.get('text'):
            continue

        if "c4bot" in message.get('text'):
            echo(message)

        if re.match(r"^(?!http(s)*:)\w+\.(jpg|jpeg|png|gif)$", message.get('text')):
            responseSticker(message)

    # catech all the error and move the task to queue_fail
    # except slack.errors.SlackApiError as e:
    except BaseException as e:
        print(e)
        os.rename(name, "queue_fail/" + name[6:])
        continue

    # Success
    os.remove(name)
    print("OK")
