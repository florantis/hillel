from django.contrib import admin
from .models import Student, WeekDay
# Register your models here.

class WeekDayAdmin(admin.ModelAdmin):
    list_display = ("title", "note")

class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "course")

admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(Student, StudentAdmin)