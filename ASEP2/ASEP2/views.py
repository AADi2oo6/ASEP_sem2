from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages #for Alert messages
from login.models import login

Role = ""
def index(request):
    return render(request,"index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        r = request.POST.get('role')

        # password = request.POST['password']
        users = login.objects.filter(userName=username)
        if users.exists() and users.first().role == r.lower():
            if users.first().Password == password:
                global Role
                Role = r
                messages.success(request, "Login successful!")
            else:
                messages.error(request,"Incorrect Password!")
        else :
            messages.error(request,"Username Not Fount!")

    return render(request, "INDEX.html")