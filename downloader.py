from __future__ import print_function

from datetime import datetime, timedelta
from collections import defaultdict
import os.path
import json
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        timeMax = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting upcoming events')
        events_result = service.events().list(calendarId='primary',
                                              timeMin=now,
                                              timeMax=timeMax,
                                              maxResults=100,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        print(events)

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(event['summary'], "from", start, "to", end)
            

        # Bin by event (aka instructor) name
        output = my_dict = defaultdict(list)
        for event in events:
            name = event["summary"]
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            output[name].append([start, end])
            
        with open("availabilities.json", "w") as f:
            json.dump(output, f, indent=4)

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
