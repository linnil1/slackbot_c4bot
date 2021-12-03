# c4bot: Slack bot for c4lab

## Feature
* Meeting notification from Google Sheet
* Add emoji of word(chinese) by command

## Install

``` bash
git clone git@github.com:linnil1/slackbot_c4bot.git
cd slackbot_c4bot
```

Note: I tested on python3.10

## Setting

### Slack

Install your own app. [tutorial](https://api.slack.com/start/building/bolt-python)

Go to [Slack API site](https://api.slack.com/), configure the app you choose and

set Event API Request URL `https://{host}:{port}/slack/events`

with scope
```
app_mentions:read
commands
im:read
im:write
reactions:read
reactions:write
users:read
emoji:read
```

and slash command
``` yml
  slash_commands:
    - command: /emojiword
      url: https://{host}:{port}/slack/events
      description: Add emoji of word
      usage_hint: "[emoji_name] [emoji_text(allow newline)]"
      should_escape: false
```

### Google

Create new project. [turoial](https://developers.google.com/workspace/guides/create-project)

Go to [GCP console](https://console.cloud.google.com/apis/credentials), choose the app you create and

enable google sheet api and create a APIkey


## Run
Edit `configuration.example.py` to `configuration.py`

``` bash
pip3 install -r requirments.txt
python3 app.py
```

or run in docker

``` bash
docker build . -t linnil1/c4bot
docker run -d --restart always -v $PWD:/app -w /app -p 80:80 --name c4bot linnil1/c4bot
```

## Warning

Setup a webserver like nginx or apache and trun on ssl(https), don't expose the endpoint with plain text

## Result
1. Emojiword
![](https://raw.githubusercontent.com/linnil1/slackbot_c4bot/main/emojiword.png)
2. Auto meeting nofication
![](https://raw.githubusercontent.com/linnil1/slackbot_c4bot/main/automeetnotify.png)
