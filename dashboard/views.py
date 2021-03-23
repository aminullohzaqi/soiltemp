from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from inputForm import models

# Create your views here.

def graph(request) :
    graph_data = models.SoilTempModel.objects.order_by('-published')[:5:-1]
    gauge_data = models.SoilTempModel.objects.order_by('-published')[0:1]
    
    admin_group = Group.objects.get(name='administrator')
    staff_group = Group.objects.get(name='staff_stasiun')
    visitor_group = Group.objects.get(name='user_visit')
    
    all_group  = request.user.groups.all()

    sidenav = None
    template_name = None

    if request.user.is_authenticated:
        template_name = 'dashboard/graph.html'
        if admin_group in all_group:
            sidenav = "dashboard/snippets/sidenav_dashboard.html"
        elif staff_group in all_group:
            sidenav = "dashboard/snippets/sidenav_dashboard.html"
        elif visitor_group in all_group:
            sidenav = "dashboard/snippets/sidenav_dashboard_user.html"
    else:
        return redirect('index')
    #error = ""
    context = {
        'judul': 'Graph Data',
        'graph_data': graph_data,
        'gauge_data': gauge_data,
        'all_group': all_group,
        'admin_group': admin_group,
        'staff_group': staff_group,
        'visitor_group': visitor_group,
        'sidenav': sidenav,
    }
    
    return render(request, template_name, context)