import os
import asyncio
import logging
import aiocron
from aiohttp import web
from slack_bolt.async_app import AsyncApp

from emoji_word import Emoji
from google_sheet import GoogleSheet
import configuration


logging.basicConfig(level=logging.DEBUG)
app = AsyncApp(token=configuration.token,
               signing_secret=configuration.signing_secret)
loop = asyncio.new_event_loop()


@aiocron.crontab(configuration.meeting_cron, loop=loop)
async def cron_meeting_notify():
    """ Run meeting noficiation every week """
    await GoogleSheet().main()


@app.event("message")
async def event_read_message(body, say, logger):
    # logger.info(body)
    pass


@app.event("app_home_opened")
async def handle_app_home_opened_events(body, say, logger):
    await say(blocks=[
        {
            'type': "section",
            'text': {
                'type': "mrkdwn",
                'text': "Hi. I'm c4bot, a specific bot for c4lab\n"
                        "Here is my repo "
                        "<https://github.com/linnil1/slackbot_c4bot>"
            },
        },
    ])
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
    # Run aiocron with aiohttp
    # The original app.start() will use two different event loop
    # so I run app.start() by myself
    # https://github.com/slackapi/bolt-python/blob/main/slack_bolt/app/async_server.py
    web.run_app(app.server().web_app,
                port=configuration.web_port,
                loop=loop)
