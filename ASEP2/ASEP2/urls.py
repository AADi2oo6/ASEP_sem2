"""
URL configuration for ASEP2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ASEP2 import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name = "index"),
    # path("",views.login_view,name= "index"),
    path("logOut/",views.logout_views,name="logout"),
    path('dashboard/', views.login_view, name='login'),
    path("student_schedule/",views.schedule),
    path("schedule/",views.schedule),
    path("buildingpage",views.buildingpage),
    path("rooms",views.rooms),
    path("floor",views.floor),
    path("freeclassrooms",views.freeclassrooms),
    # path("faculty_timetable",views.faculty_timetable),
    path("faculty_timetable",views.timeTalbe),
    path("branchschedule",views.branchschedule),
    path("announcements",views.announcements),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
