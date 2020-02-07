from pprint import pprint
import slack
import json
import os
import time
import re

import configuration
import sticker
import door_open

token = configuration.token
client = slack.WebClient(token=token)
sticker_regex = re.compile(r"^(?!http(s)*:).+\.(jpg|jpeg|png|gif)$")


def readName(id):
    response = client.users_info(user=id)
    return response.data['user']['profile']['display_name']


def echo(message):
    """Echo to person who call c4bot"""
    rep = {
        'channel': message['channel'],
        'text': f"Hello <@{message['user']}>!",
    }
    if message.get('thread_ts'):
        rep['thread_ts'] = message['thread_ts']

    response = client.chat_postMessage(**rep)
    pprint(response['message'])
    print("Response Done")


def stickerResponse(message):
    """Google Search a image"""
    keyword = message.get("text")
    url = sticker.imageSearch(keyword)
    text = keyword + f" from " + readName(message['user'])
    blocks = sticker.imageBlock(text, url)

    response = client.chat_postMessage(
                   channel=message['channel'],
                   blocks=blocks)
    pprint(response['message'])
    print("Response Done")


def doorOpen(message):
    reaction = "x"
    if door_open.doorOpen():
        reaction = "heavy_check_mark"
    response = client.reactions_add(
            name=reaction,
            channel=message['channel'],
            timestamp=message['ts'])
    pprint(response['message'])
    print("Response Done")


def success(name):
    os.remove(name)
    print("OK")


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
        # not text
        if message.get('subtype') or message.get('bot_id') \
                or not message.get('text'):
            success(name)
            continue

        if "c4bot" in message.get('text'):
            echo(message)

        # not in thread
        if message.get('thread_ts'):
            success(name)
            continue

        if sticker_regex.match(message.get('text')):
            stickerResponse(message)

        if message.get('channel') == configuration.channel_testing and \
           message.get('text') == configuration.door_message:
            doorOpen(message)

    # catech all the error and move the task to queue_fail
    # except slack.errors.SlackApiError as e:
    except BaseException as e:
        print(e)
        os.rename(name, "queue_fail/" + name[6:])
        """
        response = client.chat_postMessage(
                        text=str(message) + " : " + str(e),
                        channel=configuration.channel_testing)
        """
        continue

    # Success
    success(name)
