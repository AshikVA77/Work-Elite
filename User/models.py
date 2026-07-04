from django.db import models
from Company.models import *
# Create your models here.
class tbl_request(models.Model):
    request_date=models.DateField(auto_now_add=True)
    request_status=models.IntegerField(default=0)
    job=models.ForeignKey(tbl_job,on_delete=models.CASCADE)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)

class tbl_feedback(models.Model):
    feedback_content=models.CharField(max_length=50)
    feedback_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)

class tbl_complaints(models.Model):
    complaint_title=models.CharField(max_length=50)
    complaint_content=models.CharField(max_length=50)
    complaint_date=models.DateField(auto_now_add=True)
    complaint_status=models.IntegerField(default=0)
    complaint_replay=models.CharField(max_length=60)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    Company=models.ForeignKey(tbl_company,on_delete=models.CASCADE,null=True)

class tbl_payment(models.Model):
    payment_date=models.DateField(auto_now_add=True)
    payment_enddate=models.DateField()
    payment_status=models.IntegerField(default=0)
    user=models.ForeignKey(tbl_user,on_delete=models.CASCADE)