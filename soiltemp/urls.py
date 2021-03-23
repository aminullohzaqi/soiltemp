
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('logout/', views.logoutView, name="logout"),
    path('dashboard/', include('dashboard.urls')),
    path('input-form/', include('inputForm.urls')),
    path('logdata/', include('logdata.urls')),
    path('about/', include('about.urls')),
]
