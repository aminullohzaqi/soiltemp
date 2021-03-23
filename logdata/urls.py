from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.logdata, name="logdata"),
    path('delete/<int:delete_id>/', views.delete, name="delete"),
    path('update/<int:update_id>/', views.update, name="update"),
]