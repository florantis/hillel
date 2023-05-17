"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('choose_course/', views.choose_course, name="choose_course"),
    path('choose_course/done/', views.course_ok, name="course_chosen"),
    path('grade/', views.grade, name="grade"),
    path('', views.index, name="index" ),

    path('my_week/', views.show_week, name="week"),
    path('my_week/day/<int:day>/', views.show_day, name="day_notes"),
    path('my_week/day/<int:day>/note/<int:note_id>/', views.show_note, name="note"),
]
