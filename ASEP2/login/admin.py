from django.contrib import admin
from login.models import login,Flogin
# Register your models here.
class loginAdmin(admin.ModelAdmin):
    list_display = ['id',"Name","semester","year","userName","Password",'course_name',"batch","div"]
admin.site.register(login,loginAdmin)

class FloginAdmin(admin.ModelAdmin):
    list_display = ["id","teachersID","Name","userName","Password"]
admin.site.register(Flogin,FloginAdmin)
