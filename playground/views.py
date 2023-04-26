from google.oauth2.credentials import Credentials
from django.shortcuts import redirect
from google_auth_oauthlib.flow import Flow
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.shortcuts import render
import json

GOOGLE_CLIENT_ID = '893212124283-54cvtl3i6bh71t6sdmtdvjjcuatjefek.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

# Create your views here.
# View function is a function that takes a web request and returns a web response.
# Request handler
# Action handler


# First view function
# def say_hello(request):
#     return HttpResponse('Hello, World!')

def say_hello(request):
    return render(request, 'hello.html', {'name': 'Gaurav'})


# def GoogleCalendarInitView(request):
#     # This funciton should prompt user for his/her credentials
#     return HttpResponse('Google Calendar Init View')

def GoogleCalendarInitView(request):
    flow = Flow.from_client_config(
        client_config={
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uris': ['http://localhost:8000/rest/v1/calendar/oauth2callback'],
            'scope': ['https://www.googleapis.com/auth/calendar.events.readonly']
        },
        scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
        state='google_auth_state'
    )
    auth_url, _ = flow.authorization_url()
    request.session['google_auth_state'] = flow.state
    return redirect(auth_url)


# def GoogleCalendarRedirectView(request):
#     # Handle redirect request sent by google with code for token. You need to implement mechanism to get access_token from given code
#     # Once got the access_token get list of events in users calendar
#     return HttpResponse('Google Calendar Redirect View')


def oauth2callback(request):
    flow = Flow.from_client_config(
        client_config={
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uris': ['http://localhost:8000/rest/v1/calendar/oauth2callback'],
            'scope': ['https://www.googleapis.com/auth/calendar.events.readonly']
        },
        scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
        state=request.session.get('google_auth_state', '')
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    request.session['google_auth_credentials'] = credentials.to_json()
    return redirect('event_list')


def event_list(request):
    credentials = Credentials.from_authorized_user_info(
        info=json.loads(request.session['google_auth_credentials']))
    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary', maxResults=10,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    context = {'events': events}
    return render(request, 'event_list.html', context)
