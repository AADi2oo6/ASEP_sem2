from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages #for Alert messages
from login.models import login,Flogin
from django.forms.models import model_to_dict # using this to access the whole data of user in one go in form of dicet

from datetime import datetime


def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        r = request.POST.get('role')

        if r == "Student":
            user_qs = login.objects.filter(userName=username)
        else:
            user_qs = Flogin.objects.filter(userName=username)

        if user_qs.exists():
            user = user_qs.first()
            if user.Password == password:
                # request.session['branch'] = user.branch  # these are the global veriable now which can be acessed using "request.session.get("column name")"
                request.session['role'] = r
                request.session['username'] = user.userName

                request.session['user'] = model_to_dict(user)# this will get deta from all the columns of the user in form of dict

                return redirect("login")
            else:
                messages.error(request, "Incorrect Password!")
        else:
            messages.error(request, "Username Not Found!")
    return render(request, "index.html")



def login_view(request):
    data = {
        "name" : request.session.get("username").split(".")[0].capitalize()
    }
    if request.session.get("role") == "Faculty":
        return render(request, "facalty_dashboard.html", data)
    else:
        return render(request, "student_dashboard.html", data)




def logout_views(request):
    request.session.flush()  # Clears all session data
    return redirect("index")  # or wherever you want to send them

def student_schedule(request):
    user_data = request.session.get("user") # this will fetch all the data of user form the session 

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = list(range(8, 18))  # 8 AM to 5 PM
    today = datetime.today().strftime("%A")  # Gets current day like 'Tuesday'
    data = {
        'days': days,
        'hours': hours,
        'today': today,
        # "student":request.session.get("branch")+ " - "+user_data["div"]
        "student": f"{user_data['branch']} - {user_data["div"]}"
    }
    return render(request, 'student_schedule.html', data)
