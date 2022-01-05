import os
import asyncio
import logging
import aiocron
from aiohttp import web, ClientSession
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
        await respond("Error format. (Correct one: emojiword broken 壞了)")
        return
    name, word = command.split(maxsplit=1)
    try:
        em = Emoji(name, word)
        await em.upload()
    except BaseException as e:
        await respond(f"Error {str(e)}")
        return

    await respond(f"OK Here you are :{em.name}:")


async def incomingProxy(request):
    """
    Proxy QNAP notification to slack incoming webhook

    see https://hackmd.io/pMRmdzpuTGO9yMWXQleRwA
    """
    async with ClientSession() as session:
        rep = await session.post(configuration.incoming_secret_slack,
                                 json={'text': request.query.get("text", "")})
        return web.json_response({"status": "ok", 'data': await rep.text()})


if __name__ == "__main__":
    # Run aiocron with aiohttp
    # https://gist.github.com/linnil1/864c384fb246919800abfee2a3803a4c
    app.server().web_app.add_routes(
            [web.get(configuration.incoming_secret, incomingProxy)])
    web.run_app(app.server().web_app,
                port=configuration.web_port,
                loop=loop)
