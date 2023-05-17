from django.contrib import admin
from .models import Student, WeekDay, Note
# Register your models here.

class WeekDayAdmin(admin.ModelAdmin):
    list_display = ("title",)

class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "language", "course")

class NoteAdmin(admin.ModelAdmin):
    list_display = ("title",)

admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Note, NoteAdmin)