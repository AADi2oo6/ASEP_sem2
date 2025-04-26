from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages #for Alert messages
from django.forms.models import model_to_dict # using this to access the whole data of user in one go in form of dicet

from login.models import login,Flogin

from TimeTable.models import StudentsTT


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
                request.session["Name"] = user.Name

                request.session['user'] = model_to_dict(user)# this will get deta from all the columns of the user in form of dict

                return redirect("login")
            else:
                messages.error(request, "Incorrect Password!")
        else:
            messages.error(request, "Username Not Found!")
    return render(request, "index.html")



def login_view(request):
    data = {
        "name" : request.session.get("Name")
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
    Class = f"{user_data['branch']} - {user_data['div']}"
    dic = {

    }
    TTd = StudentsTT.objects.filter(course_name = Class)
    print("================================================================================")
    for i in TTd:
        print(i.time_slot)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = ['8-9 AM', '9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '1-2 PM', '2-3 PM', '3-4 PM', '4-5 PM', '5-6 PM']

    dic = {}

    for i in days:
        dic[i] = {}  # Initialize empty dictionary for each day
        
        for x in hours:
            found = False
            for j in TTd:
                if i == j.day and x == j.time_slot:  
                    dic[i][x] = (j.room_no, j.subject_name, j.teacher_name, j.class_type)
                    found = True
                    break  # Once found, no need to check further

            if not found:
                dic[i][x] = ("", "", "", "")  # Empty values if no class
    today = datetime.today().strftime("%A")  # Gets current day like 'Tuesday'
    data = {
        'days': days,
        'hours': hours,
        'today': today,
        # "student":request.session.get("branch")+ " - "+user_data["div"]
        "class": Class,
        "batch":user_data['batch'],
        "dic":dic

    }
    return render(request, 'student_schedule.html', data)
