import datetime as dt
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_event(email, date, time, doctor):
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    event = {
        'summary': 'Health Center Appointment',
        'location': 'HC, IIT Jodhpur',
        'description': 'Appointment with {} at Health Center, IIT Jodhpur'.format(doctor),
        'start': {
            'dateTime': date+'T'+time+':00',
            'timeZone': 'Asia/Kolkata',
        },

        'end': {
            'dateTime': date+'T'+(dt.datetime.strptime(time, '%H:%M')+dt.timedelta(minutes=10)).strftime('%H:%M')+':00',
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [
            {'email': email},
        ],
    }

    event = service.events().insert(calendarId='primary', body=event, sendUpdates="all").execute()
    print('Event created: %s' % (event.get('htmlLink')))
