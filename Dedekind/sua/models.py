from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
import datetime


YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+4)):
    YEAR_CHOICES.append((r, r))


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    number = models.IntegerField(_("Student Number"))
    suahours = models.FloatField()
    name = models.CharField(max_length=100)
    grade = models.IntegerField(_("Student Grade"), choices=YEAR_CHOICES, default=datetime.datetime.now().year)

    def __str__(self):
        return self.name


class Sua(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    team = models.CharField(max_length=200, default="未分组")
    date = models.DateTimeField('活动日期')
    suahours = models.FloatField()
    last_time_suahours = models.FloatField(default=0.0)

    def __str__(self):
        return self.student.name + '的 ' + self.title

    def update_student_suahours(self):
        if self.last_time_suahours != self.suahours:
            self.student.suahours += (self.suahours - self.last_time_suahours)
            self.student.save()
            self.last_time_suahours = self.suahours
