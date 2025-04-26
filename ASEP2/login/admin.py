from django.contrib import admin
from login.models import login,Flogin
# Register your models here.

class loginAdmin(admin.ModelAdmin):
    list_display = ['id',"Name","semester","userName","Password",'branch',"div"]
admin.site.register(login,loginAdmin)

class FloginAdmin(admin.ModelAdmin):
    list_display = ["id","userName","Password"]
admin.site.register(Flogin,FloginAdmin)