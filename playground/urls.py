from django.urls import path
from . import views

# Case sensitive
# URLConf module: URL configuration
# Every app can have it's own URL configuration
# Have to import this URL configuration to the main URL configuration

# TODO: init/ :
urlpatterns = [
    path('hello/', views.say_hello),
    path('init/', views.GoogleCalendarInitView),
    # path('redirect/', views.GoogleCalendarRedirectView),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('event-list/', views.event_list, name='event_list'),
]
