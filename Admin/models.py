from django.db import models


# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)

class tbl_category(models.Model):
    category_name=models.CharField(max_length=50)


class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=50)

class tbl_place(models.Model):
    place_name=models.CharField(max_length=50)
    district = models.ForeignKey(tbl_district, on_delete=models.CASCADE)

class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category = models.ForeignKey(tbl_category, on_delete=models.CASCADE)

class tbl_product(models.Model):
    product_name=models.CharField(max_length=40)
    price=models.CharField(max_length=40)
    details=models.CharField(max_length=40)
    product_photo=models.FileField(upload_to='Assets/Admin/Photos/')
    subcategory=models.ForeignKey(tbl_subcategory,on_delete=models.CASCADE)


class tbl_companytype(models.Model):
    company_type=models.CharField(max_length=30)


