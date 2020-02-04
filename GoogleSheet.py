import pickle
import os.path
import csv
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import configuration


def getSheet(id, loc):
    """
    Call api to get sheet csv data.

    More details are in https://developers.google.com/sheets/api/quickstart/python.
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('data/token.pickle'):
        with open('data/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('data/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values


def saveSheet(data):
    """Save the data to csv"""
    with open("data/tmp.csv", "w", newline='') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)


def readSheet():
    """Read data from csv"""
    with open("data/tmp.csv", newline='') as f:
        reader = csv.reader(f)
        return list(reader)


if __name__ == "__main__":
    # save sheet to csv
    SAMPLE_SPREADSHEET_ID = configuration.google_sheet_id
    SAMPLE_RANGE_NAME = configuration.google_sheet_range
    result = getSheet(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
    pprint(result)
    saveSheet(result)

    # read sheet from csv
    pprint(readSheet())
