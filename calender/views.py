import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponseRedirect
from convin.settings import GOOGLE_OAUTH_JSON, GOOGLE_OAUTH_REDIRECT_URI, OAUTH_SCOPES

import google_auth_oauthlib.flow
from googleapiclient.discovery import build

# Create your views here.
class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            GOOGLE_OAUTH_JSON,
            scopes = OAUTH_SCOPES)
        flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')
    
        return HttpResponseRedirect(authorization_url)

class GoogleCalendarRedirectView(APIView):
    def get(self,request):
        try:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                GOOGLE_OAUTH_JSON,
                scopes=OAUTH_SCOPES,
            )

            flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI
            authorization_response = request.build_absolute_uri()
            flow.fetch_token(authorization_response=authorization_response)

            credentials = flow.credentials

            calendar_service = build('calendar', 'v3', credentials=credentials)
            now = datetime.datetime.utcnow().isoformat() + 'Z'

            events_result = calendar_service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            if not events:
                return Response('No upcoming events found.')

            else:
                return Response(events)

        except Exception as e:
            return Response(str(e), status=400)



    