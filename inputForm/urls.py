from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.inputform, name="input"),
]