from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages #for Alert messages
from django.forms.models import model_to_dict # using this to access the whole data of user in one go in form of dicet

from login.models import login,Flogin

from TimeTable.models import StudentsTT,FacultysTT
# StudentsTT.objects.all().update(course_name= "AI")
import os
os.chdir("C:\\Users\\adish\\OneDrive\\Documents\\GitHub\\ASEP_sem2\\ASEP2")



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
                if r == "Faculty":
                    request.session["TeachersID"] = user.teachersID
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


def schedule(request):
    data ={}
    user_data = request.session.get("user") # this will fetch all the data of user form the session 
     
    if request.session.get("role") == "Faculty":
        TTd = FacultysTT.objects.filter(teachersID = user_data["teachersID"])
        data["teachersId"]=user_data["teachersID"]      
    else: 
        TTd = StudentsTT.objects.filter(course_name=user_data["course_name"], div=user_data["div"])
        data["class"] = f"{user_data['course_name']} - {user_data['div']}"
        data["batch"] = user_data["batch"]


    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = ['8-9 AM', '9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '1-2 PM', '2-3 PM', '3-4 PM', '4-5 PM', '5-6 PM','6-7 PM','7-8 PM']

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
    today = datetime.today().strftime("%A")
    
    data1 = {
        "Name" : user_data["Name"],
        "Role":request.session.get("role"),
        'days': days,
        'hours': hours,
        'today': today,
        "dic":dic

    }
    data.update(data1)
    return render(request, 'student_schedule.html', data)



def faculty_timetable(request):
    selected_faculty = request.GET.get('faculty', '')
    timetable = {}  # Your logic to fetch timetable based on faculty
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    hours = ['8-9 AM', '9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '1-2 PM', '2-3 PM', '3-4 PM', '4-5 PM', '5-6 PM','6-7 PM','7-8 PM']

    # `timetable` should be in the format:
    # {'Monday': {'9:00-10:00': ('RoomNo', 'Subject', 'FacultyName', 'ClassType'), ...}, ...}

    return render(request, 'facusearch.html', {
        'selected_faculty': selected_faculty,
        'dic': timetable,
        'days': days,
        'hours': hours,
        # 'today': timezone.now().strftime('%A'),
    })
def timeTalbe(request):

    
    fdata = Flogin.objects.all()
    return render(request, "FacultyTimetable.html", {"Names": fdata})  # Pass Names to the template



def buildingpage(request):
  return render(request, 'buildingpage.html')

def rooms(request):
    rooms = range(1, 31)  # Create list of room numbers 1 to 30
    return render(request, 'rooms.html', {'rooms': rooms})

def floor(request):
    return render(request, 'floor.html')

def freeclassrooms(request):
     availability = {
        '1': ['101', '102', '103'],
        '2': ['201', '202'],
        '3': [],
        '4': ['401', '402', '403', '404'],
    }
     return render(request, 'freeclassrooms.html', {'availability': availability})

def branchschedule(request):
    return render(request,'branchschedule.html')

def announcements(request):
    return render(request,'announcements.html')
