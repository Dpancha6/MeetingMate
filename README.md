# MeetingMate

MeetingMate is a Google Calendar Automation Tool that seamlessly integrates with the Google Calendar API and Gmail API. The primary objective is to send timely reminders to all attendees of upcoming events scheduled on the user's Google Calendar.

<img width="500" alt="Login" src="https://github.com/Dpancha6/MeetingMate/assets/89943583/014bc2cd-ac45-428a-bf15-b2b600942c25">

<img width="500" alt="homepage" src="https://github.com/Dpancha6/MeetingMate/assets/89943583/0bf1befd-6e81-49b5-abcf-ff6827dc40d0">

<img width="500" alt="AllMeetings" src="https://github.com/Dpancha6/MeetingMate/assets/89943583/922f7d93-2ab3-4ede-bdd2-e7286b9a6ee0">

## Features

- Authenticate using Google OAuth 2.0
- Fetch upcoming events from Google Calendar
- Send reminder emails to event attendees

## Prerequisites

- Python 3.x
- Google Cloud account

## Setup

1. **Clone the repository**:
   git clone https://github.com/your-username/meetingmate.git
   cd meetingmate

2. **Create and activate a virtual environment**:
- python -m venv venv
- source venv/bin/activate
- On Windows use `venv\Scripts\activate`

3. **Install the required packages**:
   pip install -r requirements.txt

4. **Run the Flask application**:
   python app.py

5. **Open your browser and navigate to `http://localhost:8000`**:
   - Click on "Authorize Google Account" and complete the OAuth 2.0 flow.
   - Visit `http://localhost:8000/events` to see the upcoming events.
   - Visit `http://localhost:8000/send_reminders` to send reminder emails to attendees.

## Usage

- **Home**: Authorize your Google account.
- **Upcoming Events**: Fetch and display upcoming events from your Google Calendar.
- **Send Reminders**: Send reminder emails to event attendees.
