from django.contrib import admin
from login.models import login
# Register your models here.

class loginAdmin(admin.ModelAdmin):
    list_display = ['id',"role","userName","Password"]
admin.site.register(login,loginAdmin)