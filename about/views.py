from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

# Create your views here.
def about(request):
    admin_group = Group.objects.get(name='administrator')
    staklim_group = Group.objects.get(name='staff_staklim')
    stamet_group = Group.objects.get(name='staff_stamet')
    
    all_group  = request.user.groups.all()

    sidenav = "about/snippets/sidenav_about.html"
    template_name = None

    if request.user.is_authenticated:
        template_name = 'about/about.html'
        if staklim_group in all_group:
            template_name = "about/aboutstaklim.html"
        elif stamet_group in all_group:
            template_name = "about/aboutstamet.html"
    else:
        return redirect('index')
    
    context = {
        'judul': 'About',
        'all_group': all_group,
        'admin_group': admin_group,
        'stamet_group': stamet_group,
        'staklim_group': staklim_group,
        'sidenav': sidenav,
    }
   
    return render(request, template_name, context)
