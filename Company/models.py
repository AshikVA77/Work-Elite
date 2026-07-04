from django.db import models
from Admin.models import *
from Guest.models import *

# Create your models here.
class tbl_jobgroup(models.Model):
    job_group=models.CharField(max_length=40)

class tbl_jobtype(models.Model):
    job_type=models.CharField(max_length=40)

class tbl_job(models.Model):
    job_title=models.CharField(max_length=40)
    job_details=models.CharField(max_length=50)
    job_date=models.DateField(auto_now_add=True)
    job_lastdate=models.DateField()
    job_qualification=models.CharField(max_length=50)
    job_status=models.IntegerField(default=0)
    job_salary=models.CharField(max_length=50)
    company=models.ForeignKey(tbl_company,on_delete=models.CASCADE)
    jobtype=models.ForeignKey(tbl_jobtype,on_delete=models.CASCADE)
    jobgroup=models.ForeignKey(tbl_jobgroup,on_delete=models.CASCADE,null=True)

class tbl_materials(models.Model):
    material_file=models.FileField(upload_to='Assets/Admin/Materials/')
    jobgroup=models.ForeignKey(tbl_jobgroup,on_delete=models.CASCADE)

class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    user_review=models.CharField(max_length=500)
    company=models.ForeignKey(tbl_company,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)