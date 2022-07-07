from django.urls import path
from calender.views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('init/', GoogleCalendarInitView.as_view(), name='index'),
    path('redirect/', GoogleCalendarRedirectView.as_view(), name='calendar'),
]