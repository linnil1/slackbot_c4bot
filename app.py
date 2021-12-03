import os
import logging
from slack_bolt.async_app import AsyncApp

from emoji_word import Emoji
import configuration

logging.basicConfig(level=logging.DEBUG)
app = AsyncApp(token=configuration.token,
               signing_secret=configuration.signing_secret)


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
    app.start(port=configuration.web_port)
