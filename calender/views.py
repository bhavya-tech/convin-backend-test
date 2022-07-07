from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

from django.shortcuts import HttpResponseRedirect
from convin.settings import JSON_FILEPATH, GOOGLE_OAUTH_REDIRECT_URI, SCOPES

import google.oauth2.credentials
import google_auth_oauthlib.flow

# Create your views here.
class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            JSON_FILEPATH,
            scopes = SCOPES)
        flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')
    
        return HttpResponseRedirect(authorization_url)

class GoogleCalendarRedirectView(APIView):
    def get(self,request):
        try:
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                JSON_FILEPATH,
                scopes=SCOPES,
            )

            flow.redirect_uri = GOOGLE_OAUTH_REDIRECT_URI
            authorization_response = request.build_absolute_uri()
            flow.fetch_token(authorization_response=authorization_response)

            credentials = flow.credentials

            return HttpResponse(credentials.to_json())
        except Exception as e:
            return HttpResponse(e)



    