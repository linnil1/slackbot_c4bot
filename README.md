# c4bot: Slack bot for c4lab

## Setup
* Custom Slackbot
* Google sheet api
* Google custom search engine and key
* ssl certification

Example of data dictionary
```
data/
├── fullchain.pem     # ssl cert
├── privkey.pem       # ssl key
└── credentials.json  # googlesheet key
```

and edit `configuration.example.py` to `configuration.py`

Final step: install python package dependency

`pip3 install requirments.txt`


## Feature
* Using webhook get the event from slack
* Google search image for you. e.g. `我就爛.jpg`
* Meeting notification from Google Sheet


## Usage
This app can run in two separate threads.
`app.py` is the webserver to collect message events.
`app_backgroud.py` response from message events.

```
python3 app.py
python3 app_backgroud.py
```
