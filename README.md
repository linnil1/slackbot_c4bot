# c4bot: Slack bot for c4lab

## Setup
* Custom Slackbot
* Google sheet api
* Google custom search engine and key
* ssl certification
* crontab
* Door opening webserver that receive door opening signal
* Create slack commands.

* Example of data dictionary
```
data/
├── fullchain.pem     # ssl cert
├── privkey.pem       # ssl key
└── credentials.json  # googlesheet key
```

* Edit `configuration.example.py` to `configuration.py`

* Add meeting notification by crontab

`crontab job.txt`

* Install python package dependency

`pip3 install requirments.txt`

* Create door server self-signed ssl

`openssl req -subj '/CN=localhost' -x509 -newkey rsa:2048 -nodes -days 365 -keyout data/self_key.pem -out data/self_cert.pem`


## Feature
* Using webhook get the event from slack
* Google search image for you. e.g. `我就爛.jpg`
* Meeting notification from Google Sheet
* Open the door by specific command
* Add emoji of word(chinese) by command


## Usage
This app can run in two separate threads.
`app.py` is the webserver to collect message events.
`app_backgroud.py` response from message events.

```
python3 app.py
python3 app_backgroud.py
```

The example of door opening server is at `door_server.py`
