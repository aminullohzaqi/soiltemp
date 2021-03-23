from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate

# Create your views here.
def about(request):
    admin_group = Group.objects.get(name='administrator')
    staff_group = Group.objects.get(name='staff_stasiun')
    visitor_group = Group.objects.get(name='user_visit')
    
    all_group  = request.user.groups.all()

    sidenav = None
    template_name = None

    if request.user.is_authenticated:
        template_name = 'about/about.html'
        if admin_group in all_group:
            sidenav = "about/snippets/sidenav_about.html"
        elif staff_group in all_group:
            sidenav = "about/snippets/sidenav_about.html"
        elif visitor_group in all_group:
            sidenav = "about/snippets/sidenav_about_user.html"
    else:
        return redirect('index')
    
    context = {
        'judul': 'About',
        'all_group': all_group,
        'admin_group': admin_group,
        'staff_group': staff_group,
        'visitor_group': visitor_group,
        'sidenav': sidenav,
    }
   
    return render(request, template_name, context)
