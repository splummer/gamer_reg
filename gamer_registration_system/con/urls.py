from django.urls import path

from . import views

app_name = 'con'
urlpatterns = [
    # ex: /con/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /con/RG1/
    path('<slug>/', views.DetailView.as_view(), name='con-detail'),
    # ex: con/5/events
    path('<slug>/events/', views.ResultsView.as_view(), name='results'),
    # handles input from events list signup
    path('<str:convention_key>/signup', views.signup, name='signup'),
]
