from django.urls import path

from . import views

app_name = 'con'
urlpatterns = [
    # ex: /con/
    path('', views.ConventionIndexView.as_view(), name='conventions'),
    # ex: /con/RG1/
    path('<slug>/', views.ConventionDetailView.as_view(), name='convention-detail'),
    # ex: con/RG1/event/1
    path('<str:convention_key>/event/<pk>', views.EventDetailView.as_view(), name='event-detail'),
    # ex: con/RG1/events
    path('<slug>/events/', views.ResultsView.as_view(), name='results'),
    # ex: con/RG1/submit_event
    path('<str:convention_key>/submit_event/', views.EventCreateView.as_view(), name='submit-event'),
    # handles input from events list signup
    path('<str:convention_key>/signup', views.signup, name='signup'),
]
