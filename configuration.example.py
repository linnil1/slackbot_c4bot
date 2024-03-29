token    = "xoxb-"               # Slackbot token
web_port = 80                    # Internal port, should proxy behind nginx
signing_secret = ""              # Slackbot signing secret (for event subscription)
user_token = "xoxc-"             # The user token with permission to upload emoji
cookie = ""                      # The cookie of the user, this is a temporary fixed for uploading emoji
google_key = ""                  # API key to read google sheet
google_sheet_id = ""             # google sheet id
google_sheet_range = '110-1 MeetingDate!A1:D23'  # google sheet range
meeting_start_year = 2021        # Our meeting year and time
meeting_start_hour = 12          # because only month and day are shown in the sheet
meeting_start_minutes = 30       # so, it's bruteforce.
meeting_channel = "lab-meeting"  # slack channel for posting meeting message
meeting_cron = "0 9 * * 3"       # Every Wednesday 17:00
incoming_secret = "/xxxxxxxxxxx" # For QNAP slack notification
incoming_secret_slack = "https://hooks.slack.com/services/Txxx"  # incoming webhook
