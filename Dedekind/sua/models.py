from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from sua.storage import FileStorage
import datetime


YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year + 4)):
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
    grade = models.IntegerField(
        _("Student Grade"),
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year
    )

    def __str__(self):
        return self.name


class SuaGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.is_staff:
            result = '院内：' + self.name
        else:
            result = '院外：' + self.name
        return result


class Sua(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(SuaGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    team = models.CharField(max_length=200, default="无分组")
    date = models.DateTimeField('活动日期')
    suahours = models.FloatField()
    last_time_suahours = models.FloatField(default=0.0)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name + '的 ' + self.title

    def clean_suahours(self):
        self.student.suahours -= self.last_time_suahours
        self.student.save()
        self.last_time_suahours = 0.0

    def update_student_suahours(self):
        if self.last_time_suahours != self.suahours:
            self.clean_suahours()
            self.student.suahours += self.suahours
            self.student.save()
            self.last_time_suahours = self.suahours


class Proof(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField('生成日期')
    is_offline = models.BooleanField(default=False)
    proof_file = models.FileField(
        upload_to='proofs',
        storage=FileStorage(),
        blank=True,
    )

    def __str__(self):
        if self.is_offline:
            return '线下证明'
        else:
            return self.user.username +\
                '_' +\
                self.date.strftime("%Y%m%d%H%M%S")


class Sua_Application(models.Model):
    sua = models.OneToOneField(
        Sua,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField('申请日期')
    detail = models.CharField(max_length=400)
    contact = models.CharField(max_length=100, blank=True)
    proof = models.ForeignKey(Proof, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    feedback = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return self.sua.student.name + '的 ' + self.sua.title + '的 ' + '申请'


class GSua(models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(SuaGroup, on_delete=models.CASCADE)
    suas = models.ManyToManyField(Sua)
    date = models.DateTimeField('活动日期')
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name + '的 ' + self.title + '的活动'


class GSuaPublicity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gsua = models.ForeignKey(GSua, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    detail = models.CharField(max_length=400)
    contact = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    published_begin_date = models.DateTimeField('开始公示时间')
    published_end_date = models.DateTimeField('结束公示时间')

    def __str__(self):
        return str(self.gsua) + '的公示'


class Appeal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField('申诉日期')
    sua = models.ForeignKey(Sua, on_delete=models.CASCADE, null=True, blank=True)
    gsua = models.ForeignKey(GSua, on_delete=models.CASCADE, null=True, blank=True)
    claim = models.CharField(max_length=400)
    reason = models.CharField(max_length=400)
    is_passed = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    feedback = models.CharField(max_length=400, blank=True)

    def __str__(self):
        if self.sua is not None:
            return self.student.name + '的“' + self.sua.title + '”的申诉'
        elif self.gsua is not None:
            return self.student.name + '的“' + self.gsua.title + '”的申诉'
        else:
            return self.student.name + '的申诉'
