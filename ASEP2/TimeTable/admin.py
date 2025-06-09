from django.contrib import admin
from .models import StudentsTT,FacultysTT,TempFacultysTT,CanceledClass
import re
from datetime import datetime, timedelta

@admin.register(StudentsTT)
class StudentsTTAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        try:
            last_entry = StudentsTT.objects.latest('id')
            
            # Extract last time_slot
            last_slot = last_entry.time_slot  # example: "8-9 AM"
            
            # Smartly calculate the next slot
            new_slot = self.increment_time_slot(last_slot)
            
            return {
                "year":last_entry.year,
                'course_name': last_entry.course_name,
                "div": last_entry.div,
                'semester': last_entry.semester,
                'day': last_entry.day,
                'time_slot': new_slot,  # 🛠️ auto incremented time slot
                'room_no': last_entry.room_no,
                'teacher_name': last_entry.teacher_name,
                'class_type': last_entry.class_type,
                'subject_name': last_entry.subject_name,

            }
        except StudentsTT.DoesNotExist:
            return super().get_changeform_initial_data(request)

    list_display = ('id', "day", "course_name","div","semester","year", "time_slot", "room_no", "subject_name", "teacher_name", "class_type",'batch')
    list_filter = ("day", "semester", "course_name", "class_type")
    search_fields = ("subject_name", "teacher_name", "course_name")

    def increment_time_slot(self, last_slot):
        """
        Takes a string like '8-9 AM' and returns '9-10 AM'
        Handles basic hour increment only (not fancy 12PM/AM switches)
        """
        match = re.match(r"(\d+)-(\d+)\s*(AM|PM)?", last_slot)
        if match:
            start_hour = int(match.group(1))
            end_hour = int(match.group(2))
            period = match.group(3) or "AM"  # default to AM if missing
            
            # Increment by 1 hour
            start_hour += 1
            end_hour += 1
            
            # Handle 12-hour format (simple logic)
            if start_hour > 12:
                start_hour -= 12
            if end_hour > 12:
                end_hour -= 12

            return f"{start_hour}-{end_hour} {period}"

        return last_slot  # fallback to same slot if parsing fails

@admin.register(FacultysTT)
class FacultysTTAdmin(admin.ModelAdmin):
    autocomplete_fields = ['teacher_name']

    def get_changeform_initial_data(self, request):
        try:
            last_entry = FacultysTT.objects.latest('id')
            
            new_slot = self.increment_time_slot(last_entry.time_slot)

            return {
                "year": last_entry.year,
                "teachersID": last_entry.teachersID,
                "course_name": last_entry.course_name,
                "div": last_entry.div,
                "semester": last_entry.semester,
                "day": last_entry.day,
                "time_slot": new_slot,
                "room_no": last_entry.room_no,
                "teacher_name": last_entry.teacher_name,
                "class_type": last_entry.class_type,
                "subject_name": last_entry.subject_name,
            }
        except FacultysTT.DoesNotExist:
            return super().get_changeform_initial_data(request)

    list_display = (
        'id', "teachersID", "day", "course_name", "div", "semester",
        "year", "time_slot", "room_no", "subject_name", "teacher_name", "class_type", 'batch'
    )
    list_filter = ("day", "semester", "course_name", "class_type")
    search_fields = ("subject_name", "course_name")

    def increment_time_slot(self, last_slot):
        import re
        match = re.match(r"(\d+)-(\d+)\s*(AM|PM)?", last_slot)
        if match:
            start_hour = int(match.group(1)) + 1
            end_hour = int(match.group(2)) + 1
            period = match.group(3) or "AM"
            if start_hour > 12:
                start_hour -= 12
            if end_hour > 12:
                end_hour -= 12
            return f"{start_hour}-{end_hour} {period}"
        return last_slot

@admin.register(TempFacultysTT)
class TempFacultysTTAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "day",
        "time_slot",
        "room_no",
        "subject_name",
        "teachersID",
        "teacher_name",
        "year",
        "class_type",
        "course_name",
        "division",
        "batch",
        "start_date",
        "end_date"
    ]

@admin.register(CanceledClass)
class CandeledClassAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "teacher_name",
        "room_no",
        "subject_name",
        "course_name", 
        'division' ,
        'batch',
        'class_type' ,
        "day",
        "time_slot",
        "start_date",
        "end_date",
        "created_at"
    ]
    search_fields = ("subject_name", "course_name","room_no")

