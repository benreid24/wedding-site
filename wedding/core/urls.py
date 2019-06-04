from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rsvp', views.rsvp, name='rsvp'),
    path('details', views.details, name='details')
]
