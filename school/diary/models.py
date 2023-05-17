from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=30)
    language = models.CharField(max_length=15)
    course = models.CharField(max_length=10)
    grade = models.IntegerField()
    
class WeekDay(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.title

class Note(models.Model):
    day = models.ForeignKey("WeekDay", on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    msg = models.CharField(max_length=256)