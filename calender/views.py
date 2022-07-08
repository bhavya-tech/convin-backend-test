import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponseRedirect
from convin.settings import GOOGLE_OAUTH_JSON, GOOGLE_OAUTH_REDIRECT_URI, OAUTH_SCOPES
import google_auth_oauthlib.flow
from googleapiclient.discovery import build


class GoogleCalendarInitView(APIView):

    def get(self, request):

        # Create flow instance to manage OAuth 2.0 Authorization Grant Flow
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            GOOGLE_OAUTH_JSON,
            scopes = OAUTH_SCOPES)
        flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI

        # Generate URL for request authorization
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')
    
        # Redirect user to OAuth 2.0 provider for authorization
        return HttpResponseRedirect(authorization_url)


class GoogleCalendarRedirectView(APIView):

    def get(self,request):

        # Attempt to validate the incoming request
        try:

            # Create flow instance for access_token
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                GOOGLE_OAUTH_JSON,
                scopes=OAUTH_SCOPES,
            )

            flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI
            authorization_response = request.build_absolute_uri()
            flow.fetch_token(authorization_response=authorization_response)

            # Extract user credentials
            credentials = flow.credentials

            # Initiate Calendar API service object
            calendar_service = build('calendar', 'v3', credentials=credentials)
            now = datetime.datetime.utcnow().isoformat() + 'Z'

            # Get 10 events from now
            events_result = calendar_service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            result = {}

            for i, event in enumerate(events):
                temp = {}
                temp['summary'] = event['summary']
                temp['start'] = event['start']['dateTime']
                temp['end'] = event['end']['dateTime']
                result[str(i+1)] = temp

            # Return events
            if not result:
                return Response('No upcoming events found.')
            else:
                return Response(result)

        # If the incoming request is not valid, return error
        except Exception as e:
            return Response(str(e), status=400)



    