from django.db import models
# Create your models here.
class Tlist(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=120, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    age = models.CharField(max_length=40, blank=True, null=True)
    expect_salary = models.CharField(max_length=60, blank=True, null=True)
    edu_exp = models.CharField(max_length=120, blank=True, null=True)
    work_exp = models.CharField(max_length=20, blank=True, null=True)
    collage = models.CharField(max_length=40, blank=True, null=True)
    professional = models.CharField(max_length=60, blank=True, null=True)
    expect_place = models.CharField(max_length=60, blank=True, null=True)
    expect_job = models.CharField(max_length=60, blank=True, null=True)
    class Meta:
        db_table = 't_resume'


class UserIP(models.Model):
    ip = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    time_now = models.CharField(max_length=100)
    visited_func = models.CharField(max_length=100)
    count = models.IntegerField()
    class Meta:
        db_table = 't_userip'