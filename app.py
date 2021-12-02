import os
# from aiohttp import web
from slack_bolt.async_app import AsyncApp
import logging

import configuration
from emoji_word import Emoji
logging.basicConfig(level=logging.DEBUG)


app = AsyncApp(token=configuration.token,
               signing_secret=configuration.signing_secret)


@app.event("message")
async def event_read_message(body, say, logger):
    logger.info(body)
    pass
    # await say("What's up?")


@app.event("app_home_opened")
async def handle_app_home_opened_events(body, say, logger):
    logger.info(body)


@app.command("/emojiword")
async def command_emojiword(ack, respond, command, say, logger):
    logger.info(respond)
    logger.info(command)
    command = command['text']
    await ack()
    if len(command.split()) < 2:
        await say("Error format. (Correct one: emojiword broken 壞了)")
        return
    name, word = command.split(maxsplit=1)
    try:
        em = Emoji(name, word)
        await em.upload()
    except BaseException as e:
        await say(f"Error {str(e)}")
        return

    await say(f"OK Here you are :{em.name}:")


if __name__ == "__main__":
    app.start(port=configuration.web_port)
