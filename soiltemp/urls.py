
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('logout/', views.logoutView, name="logout"),
    path('dashboard/', include('dashboard.urls')),
    path('input-form/', include('inputForm.urls')),
    path('logdata/', include('logdata.urls')),
    path('about/', include('about.urls')),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
