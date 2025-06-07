from django.contrib import admin
from login.models import login,Flogin
# Register your models here.
class loginAdmin(admin.ModelAdmin):
    search_fields = ['Name', 'userName', 'Password','batch']
    list_display = ['id',"Name","semester","year","userName","Password",'course_name',"batch","div"]
admin.site.register(login,loginAdmin)

class FloginAdmin(admin.ModelAdmin):
    search_fields = ['Name']
    list_display = ["id","teachersID","rank","dept","Name","userName","Password"]
admin.site.register(Flogin,FloginAdmin)
