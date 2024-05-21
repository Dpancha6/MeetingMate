from flask import Flask, redirect, url_for, session, request, render_template
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import datetime
import os
import base64
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"

CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/gmail.send']

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect('authorize')
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('index'))


@app.route('/events')
def events():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    next_week = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=now, 
                                          timeMax=next_week, 
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    if not events:
        return 'No upcoming events found.'
    
    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append({'start': start, 'summary': event['summary']})
    
    session['credentials'] = credentials_to_dict(credentials)
    return render_template('events.html', events=event_list)

@app.route('/send_reminders')
def send_reminders():
    if 'credentials' not in session:
        return redirect('authorize')
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    
    calender_service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    gmail_service = googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    next_week = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'

    events_result = calender_service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=next_week, 
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        attendees = event.get('attendees', [])
        for attendee in attendees:
            email = attendee['email']
            subject = f"Reminder: Upcoming Meeting - {event['summary']}"
            message_text = f"Hello {attendee['email']},\n\nThis is a reminder for your upcoming meeting on {start}.\n\nBest, \nMeetingMate"
            message = create_message(email, subject, message_text)
            print('Message in Email: ', message , '\n\n')
            send_message(gmail_service, 'me', message)
    
    session['credentials'] = credentials_to_dict(credentials)
    return render_template('email_sent.html')

def create_message(to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}



if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8000, debug=True)
