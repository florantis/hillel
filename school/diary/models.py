from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=30)
    language = models.CharField(max_length=15)
    course = models.CharField(max_length=10)
    grade = models.IntegerField()
    
class WeekDay(models.Model):
    title = models.CharField(max_length=20)
    note = models.CharField(max_length=250)