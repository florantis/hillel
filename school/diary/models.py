from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=30)
    language = models.CharField(max_length=15)
    course = models.CharField(max_length=10)
    grade = models.IntegerField()

    # def __init__(self, name = None, language = None):
    #     self.name = name
    #     self.language = language
    #     self.course = ""
    #     self.grade = None

    # def set_course(self, course):
    #     self.course = course 

    # def get_grade(self, grade):
    #     self.grade = grade