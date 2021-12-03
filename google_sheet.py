from datetime import datetime, timedelta
from pprint import pprint
from slack_sdk.web.async_client import AsyncWebClient
from aiogoogle import Aiogoogle

import configuration


class GoogleSheet:
    date_name = "日期"
    client = AsyncWebClient(token=configuration.token)
    timedelta_tpe = 8

    def __init__(self, channel=configuration.meeting_channel):
        self.channel = channel

    async def getRawTable(self):
        """ Get google sheet from web """
        async with Aiogoogle(api_key=configuration.google_key) as ag:
            sheet = await ag.discover('sheets', 'v4')
            result = await ag.as_api_key(
                sheet.spreadsheets.values.get(
                    spreadsheetId=configuration.google_sheet_id,
                    range=configuration.google_sheet_range)
            )
            return result['values']

    async def getTable(self):
        """ Clean data and transfer array to dict """
        tables = await self.getRawTable()
        # tables = [['周次', '日期', '報告人', '報告人'],
        #           ['', '9/1', 'xx', 'oo']]

        # add suffix for duplicated header
        header = tables[0]
        num = {}
        for i, v in enumerate(header):
            if v in num:
                num[v] += 1
                header[i] += str(num[v])
            else:
                num[v] = 0

        # add year on date string
        df = tables[1:]
        ind_date = header.index(self.date_name)
        year = configuration.meeting_start_year
        prev_date = datetime(year, 1, 1)
        for i in df:
            while True:
                tmp_date = datetime(year,
                                    int(i[ind_date].split('/')[0]),
                                    int(i[ind_date].split('/')[1]),
                                    configuration.meeting_start_hour,
                                    configuration.meeting_start_minutes)
                if tmp_date < prev_date:
                    year += 1
                else:
                    break
            i[ind_date] = prev_date = tmp_date

        # array to dict
        data = [dict(zip(header, row)) for row in df]
        return data

    async def notify(self, row):
        """
        Format the text

        Reference: https://api.slack.com/reference/block-kit/blocks
        """
        await self.client.chat_postMessage(blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Meeting 通知"
                }
            },
            *[{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{k}: *{v}*"
                }
            } for k, v in row.items()],
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "請在 Meeting 前提供 paper 的連結  "
                            "並記得把投影片放在 c4lab 的 google drive"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Notified automatically from "
                                "[c4bot](https://github.com/linnil1/slackbot_c4bot)",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "[Meeting sheet](https://docs.google.com/spreadsheets/d/" +
                                configuration.google_sheet_id + ")"
                    }
                ]
            }
        ], channel=self.channel)

    async def main(self):
        """ Download sheet and notify who will be next """
        tables = await self.getTable()
        pprint(tables)
        now = datetime.now() + timedelta(hours=self.timedelta_tpe)
        print(now)

        # find the next studuents after today's meeting
        row = list(filter(lambda i: i[self.date_name] > now, tables))
        if not len(row):
            print("Empty sheet")
            return False
        row = min(row, key=lambda i: i[self.date_name])

        await self.notify(row)
        return True


if __name__ == "__main__":
    import asyncio
    asyncio.run(GoogleSheet("DSY9Z1S8J").main())
