from datetime import datetime,date
from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseRedirect, JsonResponse
from django.contrib import messages #for Alert messages
from django.forms.models import model_to_dict # using this to access the whole data of user in one go in form of dicet
from django.utils.dateparse import parse_date

from login.models import login,Flogin

from TimeTable.models import FacultysTT,TempFacultysTT, CanceledClass

from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from announcements.models import Announcement
from django.utils import timezone
import os

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
    user = request.session.get("user")
    name = user.get("Name")
    role = request.session.get("role")

    data = {
        "name": name,
    }

    if role == "Faculty":
        return render(request, "facalty_dashboard.html", data)
    else:
        # For student, filter announcements
        year = user.get("year")
        branch = user.get("course_name")
        section = user.get("div")
        batch = user.get("batch")

        announcements = Announcement.objects.filter(
            years__icontains=year,
            branches__icontains=branch,
            sections__icontains=section,
            batches__icontains=batch
        ).order_by('-created_at')[:10]

        data["announcements"] = announcements

        return render(request, "student_dashboard.html", data)

def logout_views(request):
    request.session.flush()  # Clears all session data
    return redirect("index")  # or wherever you want to send them

def schedule(request, identifier=None):
    data = {}
    today_date = date.today()
    user_data = request.session.get("user")
    role = request.session.get("role")
    
    is_room_view = False
    TTd = []
    temp_tt = []
    canceled = []

    if identifier is None and role == "Faculty":
        teacher_name = request.session.get("Name")
        TTd = FacultysTT.objects.filter(teacher_name__Name=teacher_name)
        temp_tt = TempFacultysTT.objects.filter(teacher_name=teacher_name, end_date__gte=today_date)
        canceled = CanceledClass.objects.filter(teacher_name=teacher_name, end_date__gte=today_date)
        Name = teacher_name
        data["teachersId"] = user_data["teachersID"]
    elif identifier is None:
        # Normal student
        course = user_data["course_name"]
        div = user_data["div"]
        batch = user_data["batch"]
        TTd = FacultysTT.objects.filter(course_name=course, div=div)
        temp_tt = TempFacultysTT.objects.filter(course_name=course, division=div, end_date__gte=today_date)
        canceled = CanceledClass.objects.filter(course_name=course, division=div, batch__in=["all", batch], end_date__gte=today_date)
        Name = user_data["Name"]
        data["class"] = f"{course} - {div}"
        data["batch"] = batch
    else:
        if "-" in identifier:
            try:
                course_name, year, div = identifier.split("-")

                TTd = FacultysTT.objects.filter(course_name=course_name, div=div)
                temp_tt = TempFacultysTT.objects.filter(course_name=course_name, division=div, end_date__gte=today_date)
                canceled = CanceledClass.objects.filter(course_name=course_name, division=div, end_date__gte=today_date)

                Name = f"{course_name} {year} - {div}"
                # role = "Branch"
                data["class"] = f"{course_name} - {div}"

            except ValueError:
                return HttpResponse("Invalid identifier format.", status=400)
        else:
            try:
                # If identifier is room number (int or convertible to int)
                RoomNo = int(identifier)
                is_room_view = True
                TTd = FacultysTT.objects.filter(room_no=RoomNo)
                temp_tt = TempFacultysTT.objects.filter(room_no=RoomNo, end_date__gte=today_date)
                canceled = CanceledClass.objects.filter(room_no=RoomNo, end_date__gte=today_date)
                Name = f"Room {RoomNo}"
            except ValueError:
                # It's a faculty name
                TTd = FacultysTT.objects.filter(teacher_name__Name=identifier)
                temp_tt = TempFacultysTT.objects.filter(teacher_name=identifier, end_date__gte=today_date)
                canceled = CanceledClass.objects.filter(teacher_name=identifier, end_date__gte=today_date)
                Name = identifier
                data["teachersId"] = Flogin.objects.get(Name=identifier).teachersID if Flogin.objects.filter(Name=identifier).exists() else ""
    

    # Time table grid setup
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hours = ['8-9 AM', '9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM', '1-2 PM',
             '2-3 PM', '3-4 PM', '4-5 PM', '5-6 PM', '6-7 PM', '7-8 PM']

    dic = {day: {} for day in days}

    for day in days:
        for hour in hours:
            dic[day][hour] = ("", "", "", "", "", "", "")  # default

            cancel_entry = next((c for c in canceled if c.day == day and c.time_slot == hour), None)
            cancel_remark = f" (Canceled)" if cancel_entry else ""

            # Check temporary timetable first
            temp_entry_found = False
            for temp in temp_tt:
                if temp.day == day and temp.time_slot == hour:
                    date_range = f"{temp.start_date.strftime('%d %b')} - {temp.end_date.strftime('%d %b')}"
                    dic[day][hour] = (
                        temp.room_no,
                        temp.subject_name,
                        temp.teacher_name,
                        temp.class_type + cancel_remark,
                        temp.course_name,
                        temp.division,
                        date_range
                    )
                    temp_entry_found = True
                    break

            if not temp_entry_found:
                for entry in TTd:
                    if entry.day == day and entry.time_slot == hour:
                        dic[day][hour] = (
                            entry.room_no,
                            entry.subject_name,
                            entry.teacher_name,
                            entry.class_type + cancel_remark,
                            entry.course_name,
                            entry.div,
                            ""
                        )
                        break

    today = datetime.today().strftime("%A")

    sday = canceled.values_list('start_date', flat=True).first()
    eday = canceled.values_list('end_date', flat=True).first()

    data.update({
        "Name": Name,
        # "Role": "Faculty" if not is_room_view and role == "Faculty" else "Room",
        "Role": role,
        "days": days,
        "hours": hours,
        "today": today,
        "dic": dic,
        "sday": sday,
        "eday": eday
    })

    return render(request, 'schedule.html', data)

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

        # getting teacher info from session
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

@csrf_exempt
def cancel_schedule(request):
    if request.method == "POST":
        try:
            data = request.POST or json.loads(request.body.decode("utf-8"))

            day = data.get("day")
            time_slot = data.get("time_slot")
            cancel_type = data.get("cancel_type")
            RoomNO = data.get("room_no")
            # print("_________________________________________________________")
            # print("ROOM NO:", RoomNO)


            user = request.session.get("user")
            teacher = Flogin.objects.get(Name=user["Name"])
            teacher_id = user["teachersID"]

            # Check in TempFacultysTT first
            temp_class = TempFacultysTT.objects.filter(
                teacher_name=teacher.Name,
                teachersID=teacher_id,
                day=day,
                time_slot=time_slot,
                room_no=RoomNO
            ).first()

            if cancel_type == "temporary":
                start_date = parse_date(data.get("start_date"))
                end_date = parse_date(data.get("end_date"))

                if temp_class:
                    # Create cancel entry and delete temp class
                    CanceledClass.objects.create(
                        teacher_name=teacher,
                        room_no = RoomNO,
                        subject_name=temp_class.subject_name,
                        course_name=temp_class.course_name,
                        division=temp_class.division,
                        batch=temp_class.batch,
                        class_type=temp_class.class_type,
                        day=temp_class.day,
                        time_slot=temp_class.time_slot,
                        start_date=start_date,
                        end_date=end_date
                    )
                    temp_class.delete()
                    return JsonResponse({"success": True, "message": "Temporary class canceled."})

                # Otherwise check for permanent class
                existing_class = FacultysTT.objects.filter(
                    teacher_name=teacher,
                    day=day,
                    time_slot=time_slot,
                    room_no=RoomNO
                ).first()

                if existing_class:
                    CanceledClass.objects.create(
                        teacher_name=teacher,
                        room_no = RoomNO,
                        subject_name=existing_class.subject_name,
                        course_name=existing_class.course_name,
                        division=existing_class.div,
                        batch=existing_class.batch,
                        class_type=existing_class.class_type,
                        day=existing_class.day,
                        time_slot=existing_class.time_slot,
                        start_date=start_date,
                        end_date=end_date
                    )
                    return JsonResponse({"success": True, "message": "Permanent class temporarily canceled."})

                return JsonResponse({"success": False, "error": "Class not found to cancel temporarily."})

            else:  # Permanent cancel
                if temp_class:
                    temp_class.delete()
                    return JsonResponse({"success": True, "message": "Temporary class permanently deleted."})

                existing_class = FacultysTT.objects.filter(
                    teacher_name=teacher,
                    day=day,
                    time_slot=time_slot
                ).first()

                if existing_class:
                    existing_class.delete()
                    return JsonResponse({"success": True, "message": "Permanent class canceled."})

                return JsonResponse({"success": False, "error": "Class not found to delete permanently."})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method."})

def F_timeTalbePage(request):
    fdata = Flogin.objects.all()
    return render(request, "FacultyTimetable.html", {"Names": fdata})  # Pass Names to the template

from datetime import date  # Make sure this is imported

def RoomStatusPage(request):
    TTd = FacultysTT.objects.all()
    tempTTd = TempFacultysTT.objects.filter(end_date__gte=date.today())
    roomNO = set(
    list(FacultysTT.objects.values_list('room_no', flat=True)) +
    list(TempFacultysTT.objects.values_list('room_no', flat=True))
)


    UserData = request.session.get('user')
    role = request.session.get('role')

    now = datetime.now()
    current_day = now.strftime("%A")

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
        room_info = {
            "number": room,
            "type": "Classroom",
            "class": "",
            "teacher": "",
            "subject": "",
            "status": "vacant"
        }

        if current_slot:
            # First check in TempFacultysTT
            temp_class = tempTTd.filter(
                room_no=room,
                day=current_day,
                time_slot=current_slot,
                end_date__gte=date.today()
            ).first()

            if temp_class:
                room_info["class"] = f"{temp_class.course_name} ({temp_class.division}) , Batch : {temp_class.batch}"
                room_info["teacher"] = temp_class.teacher_name
                room_info["subject"] = f"{temp_class.subject_name} ({temp_class.class_type})"
                room_info["status"] = ""
            else:
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

    return render(request, 'RoomStatusPage.html', {
        'room_data': room_data,
        'role': role,
        "UserData": UserData
    })


def branchschedule(request):
    departments = ["CS", "CSAIML", "IT", "AIDS"]  # or dynamically from DB
    return render(request, "branchschedule.html", {"departments": departments})

def faculty_announcement(request):
    if request.method == 'POST':
        teacher = request.session.get('user')
        teacher_id = teacher.get("teachersID")
        teacher_name = teacher.get("Name")

        subject = request.POST.get('subject')
        content = request.POST.get('content')
        attachment = request.FILES.get('attachment')

        years = request.POST.getlist('year')
        branches = request.POST.getlist('branch')
        sections = request.POST.getlist('section')
        batches = request.POST.getlist('batch')

        # Save to DB
        announcement = Announcement.objects.create(
            teacher_id=teacher_id,
            teacher_name=teacher_name,
            subject=subject,
            content=content,
            attachment=attachment,
            years=years,
            branches=branches,
            sections=sections,
            batches=batches,
            created_at=timezone.now()
        )

        # ✅ Filter matching students from login model
        recipients = login.objects.filter(
            year__in=years,
            course_name__in=branches,
            div__in=sections,
            batch__in=batches
        ).values_list('userName', flat=True)

        # ✅ Send email to recipients
        if recipients:
            email = EmailMessage(
                subject=subject,
                body=content,
                from_email=settings.EMAIL_HOST_USER,
                to=list(recipients),
            )

            if attachment:
                email.attach(attachment.name, attachment.read(), attachment.content_type)

            email.send(fail_silently=False)

        messages.success(request, "✅ Announcement submitted and sent via email.")
        return redirect('announcements')

    # GET request
    announcements = Announcement.objects.all().order_by('-created_at')[:20]
    return render(request, 'announcements.html', {
        'announcements': announcements
    })