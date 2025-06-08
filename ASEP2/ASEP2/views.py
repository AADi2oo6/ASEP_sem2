from datetime import datetime,date
from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages #for Alert messages
from django.forms.models import model_to_dict # using this to access the whole data of user in one go in form of dicet
from django.utils.dateparse import parse_date

from login.models import login,Flogin

from TimeTable.models import StudentsTT,FacultysTT,TempFacultysTT


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



def schedule(request, Name=None):
    data = {}
    user_data = request.session.get("user")
    today_date = date.today()

    # --- Load permanent timetable ---
    if Name is None:
        if request.session.get("role") == "Faculty":
            TTd = FacultysTT.objects.filter(teacher_name__Name=request.session.get("Name"))
            data["teachersId"] = user_data["teachersID"]
            Name = user_data["Name"]
            temp_tt = TempFacultysTT.objects.filter(
                teacher_name=Name,
                end_date__gte=today_date  # ✅ show temp data as long as it's still valid
            )
        else:
            TTd = FacultysTT.objects.filter(course_name=user_data["course_name"], div=user_data["div"])
            Name = user_data["Name"]
            temp_tt = TempFacultysTT.objects.filter(
                course_name=user_data["course_name"],
                division=user_data["div"],
                batch__in=["all", user_data["batch"]],
                end_date__gte=today_date
            )
            data["class"] = f"{user_data['course_name']} - {user_data['div']}"
            data["batch"] = user_data["batch"]
        role = request.session.get("role")
    else:
        TTd = FacultysTT.objects.filter(teacher_name__Name=Name)
        temp_tt = TempFacultysTT.objects.filter(
            teacher_name=Name,
            end_date__gte=today_date
        )
        role = Name

    # --- Time grid ---
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = ['8-9 AM', '9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '1-2 PM',
             '2-3 PM', '3-4 PM', '4-5 PM', '5-6 PM', '6-7 PM', '7-8 PM']

    dic = {day: {} for day in days}

    for day in days:
        for hour in hours:
            # Default empty
            dic[day][hour] = ("", "", "", "", "", "")

            # 🟡 Check temp timetable first
            temp_entry_found = False
            for temp in temp_tt:
                if temp.day == day and temp.time_slot == hour:
                    # Format date range
                    date_range = f"{temp.start_date.strftime('%d %b')} - {temp.end_date.strftime('%d %b')}"
                    dic[day][hour] = (
                        temp.room_no,
                        temp.subject_name,
                        temp.teacher_name,
                        temp.class_type,
                        temp.course_name,
                        temp.division,
                        date_range
                    )
                    temp_entry_found = True
                    break

            # ⚪️ Fall back to permanent if no temp entry
            if not temp_entry_found:
                for entry in TTd:
                    if entry.day == day and entry.time_slot == hour:
                        dic[day][hour] = (
                            entry.room_no,
                            entry.subject_name,
                            entry.teacher_name,
                            entry.class_type,
                            entry.course_name,
                            entry.div
                        )
                        break

    today = datetime.today().strftime("%A")

    data.update({
        "Name": Name,
        "Role": role,
        'days': days,
        'hours': hours,
        'today': today,
        "dic": dic
    })

    return render(request, 'student_schedule.html', data)



def update_schedule(request):
    if request.method == "POST":
        day = request.POST.get("day")
        time_slot = request.POST.get("time_slot")
        class_name = request.POST.get("class_name")
        subject_name = request.POST.get("subject_name")
        division = request.POST.get("division")
        room_no = request.POST.get("room_no")
        class_type = request.POST.get("class_type")
        submit_type = request.POST.get("submit_type")
        year = request.POST.get("year")
        batch = request.POST.get("batch")

        # Assume teacher info is in session
        user = request.session.get("user")
        teacher_name = user["Name"]

        if submit_type == "temporary":
            # Parse dates
            start_date = parse_date(request.POST.get("start_date"))
            end_date = parse_date(request.POST.get("end_date"))

            TempFacultysTT.objects.create(
                teachersID= user["teachersID"],
                year = year,
                day=day,
                time_slot=time_slot,
                room_no=room_no,
                subject_name=class_name,
                teacher_name=teacher_name,
                class_type=class_type,
                course_name=class_name,
                division=division,
                start_date=start_date,
                end_date=end_date,
                batch = batch
            )
        else:
            # Save to permanent table
            obj, created = FacultysTT.objects.update_or_create(
                day=day,
                time_slot=time_slot,
                teacher_name = Flogin.objects.get(Name=user["Name"]),
                defaults={
                    'room_no': room_no,
                    'subject_name': subject_name,
                    'class_type': class_type,
                    'course_name': class_name,
                    'div': division,
                    "teachersID":user["teachersID"],
                    "year":year,
                    "batch":batch

                }
            )

        return redirect('http://127.0.0.1:8000/schedule/')  # Change to your correct schedule view name

    return redirect('http://127.0.0.1:8000/schedule/')  # fallback


def timeTalbePage(request):
    fdata = Flogin.objects.all()
    return render(request, "FacultyTimetable.html", {"Names": fdata})  # Pass Names to the template



def buildingpage(request):
    # Get all unique room numbers
    TTd = FacultysTT.objects.all()
    roomNO = TTd.values_list('room_no', flat=True).distinct()

    # Get current day and current time slot
    now = datetime.now()
    current_day = now.strftime("%A")

    # Mapping current hour to time slot
    hour_map = {
        8: '8-9 AM', 9: '9-10 AM', 10: '10-11 AM', 11: '11-12 PM',
        12: '12-1 PM', 13: '1-2 PM', 14: '2-3 PM', 15: '3-4 PM',
        16: '4-5 PM', 17: '5-6 PM'
    }
    current_hour = now.hour
    current_slot = hour_map.get(current_hour, None)

    room_data = {
        "Building 1 : DESH": [],
        "Building 2 : AIDS": [],
        "Building 3 : MECHANICAL": [],
        "Building 4 : INSTRUMENTATION": []
    }

    for room in roomNO:
        # Default values
        room_info = {
            "number": room,
            "type": "Classroom",  # Default, can adjust based on room naming if needed
            "class": "", 
            "teacher": "",
            "subject":"", 
            "status": "vacant"
        }

        if current_slot:
            scheduled = TTd.filter(room_no=room, day=current_day, time_slot=current_slot).first()
            if scheduled:
                room_info["class"] = f"{scheduled.course_name} ({scheduled.div}) , Batch : {scheduled.batch}"
                room_info["teacher"] = scheduled.teacher_name
                room_info["subject"] = f"{scheduled.subject_name} ({scheduled.class_type})"
                room_info["status"] = ""

        # Assign building
        if room.startswith("1"):
            room_info["type"] = "Classroom"
            room_data["Building 1 : DESH"].append(room_info)
        elif room.startswith("2"):
            room_info["type"] = "Lab"
            room_data["Building 2 : AIDS"].append(room_info)
        elif room.startswith("3"):
            room_info["type"] = "Workshop"
            room_data["Building 3 : MECHANICAL"].append(room_info)
        elif room.startswith("4"):
            room_info["type"] = "Classroom"
            room_data["Building 4 : INSTRUMENTATION"].append(room_info)

    return render(request, 'buildingpage.html', {'room_data': room_data})

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
