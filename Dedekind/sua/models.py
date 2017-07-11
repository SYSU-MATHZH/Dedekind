from django.db import models
from django.contrib.auth.models import User


class Sua(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sua_title = models.CharField(max_length=200)
    sua_team = models.CharField(max_length=200)
    sua_date = models.DateTimeField('活动日期')
    sua_hours = models.FloatField()

    def __str__(self):
        return self.sua_title
