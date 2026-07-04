from django.db import models
from Admin.models import *


# Create your models here

class tbl_user(models.Model):
    user_name=models.CharField(max_length=40)
    user_email=models.CharField(max_length=40)
    user_contact=models.CharField(max_length=40)
    user_address=models.CharField(max_length=50)
    user_password=models.CharField(max_length=40)
    user_photo=models.FileField(upload_to='Assets/User/Photos/')
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_status=models.IntegerField(default=0)
    user_paystatus=models.IntegerField(default=0)
    user_resume=models.FileField(upload_to='Assets/User/Resumes/')
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class tbl_company(models.Model):
    company_name=models.CharField(max_length=30)
    company_email=models.CharField(max_length=50)
    company_contact=models.CharField(max_length=50)
    company_address=models.CharField(max_length=60)
    company_password=models.CharField(max_length=50)
    company_logo=models.FileField(upload_to='Assets/Admin/logos/')
    company_licence=models.FileField(upload_to='Assets/Admin/licences/')
    company_status=models.IntegerField(default=0)
    interview_link=models.URLField(null=True)
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    companytype=models.ForeignKey(tbl_companytype,on_delete=models.CASCADE)