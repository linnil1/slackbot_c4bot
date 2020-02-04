import slack
from pprint import pprint
from datetime import datetime
import configuration


token = configuration.token
client = slack.WebClient(token=token)
channel_id = configuration.channel_meeting
# channel_id = configuration.channel_testing


def meetingBlock(date, meeting_people, comment=""):
    if not comment:
        comment = "備註 = NA"
    sections = []
    for head in meeting_people:
        if meeting_people[head]:
            sections.append(f"*{head}*: " + ", ".join(meeting_people[head]]))
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Meeting {date}"
            }
        },
        *[{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": sec
            }
        } for sec in sections],
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": comment,
                },
                {
                    "type": "mrkdwn",
                    "text": "Meeting data from https://docs.google.com/spreadsheets/d/" + configuration.google_sheet_id
                }
            ]
        }
    ]


def sendMeetingMessage():
    from GoogleSheet import readSheet
    table = readSheet()
    date, meeting_people, comment = parseData(table)
    response = client.chat_postMessage(
                   channel=channel_id,
                   blocks=meetingBlock(date, meeting_people, comment))
    pprint(response["message"])


def findDate(table):
    now = datetime.now()
    now = datetime(now.year, now.month, now.day)
    now = datetime(now.year, 2, 17)
    for i in range(1, len(table)):
        meet_month, meet_day = table[i][1].split("/")
        date  = datetime(now.year,     int(meet_month), int(meet_day))
        date1 = datetime(now.year + 1, int(meet_month), int(meet_day))
        if (date - now).days == 7 or (date1 - now).days == 7:
            return i
    raise ValueError("No Meeting is in 7 days")


def parseData(table):
    """Hard code to parse csv to slack block"""
    header = table[0]
    data = table[findDate(table)]
    # header = ['周次', '日期', '報告人', '報告人', '提問人', '提問人', '備註']
    # data = ['第一周', '2/17', 'A', 'XK', 'C', 'D', '開始第一周上課 / 若延後開學則用zoom線上視訊']
    # data = ['第八周', '4/6', '-', '-', '-', '-', '溫書假']
    date = data[0] + " " + data[1]

    meeting_people = {
            header[2]: [person for person in data[2:4] if person and person != "-"],
            header[4]: [person for person in data[4:6] if person and person != "-"],
    }
    return date, meeting_people, data[-1]


if __name__ == "__main__":
    print(sendMeetingMessage())
