from django.urls import path

from . import views

urlpatterns = [
    path('', views.graph, name="dashboard"),
]