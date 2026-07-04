from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *

def  index(request):
     return render(request,"Guest/index.html")

def  about(request):
     return render(request,"Guest/about.html")

def Login(request):
     msg2="Your company profile has been rejected. The reason has been E-mailed"
     msg1="Your Need To get Verified By Admin Before Login,Please Wait"
     msg="Your Account Has Been Blocked"
     if request.method == "POST":
          email = request.POST.get("email")
          password = request.POST.get("password")
          usercount = tbl_user.objects.filter(user_email=email,user_password=password).count()
          companycount = tbl_company.objects.filter(company_email=email,company_password=password).count()
          admincount = tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
          if usercount > 0:
               user = tbl_user.objects.get(user_email=email,user_password=password)
               if user.user_status==0:
                    request.session["uid"] = user.id
                    return redirect("User:Homepage")
               else:
                    return render(request,"Guest/Login.html",{"msg":msg})
          elif companycount > 0:
               company = tbl_company.objects.get(company_email=email,company_password=password)
               if company.company_status==0:
                    return render(request,"Guest/Login.html",{"msg1":msg1})
               elif company.company_status == 1:
                   request.session["cid"] = company.id
                   return redirect("Company:Companyhome")
               else:
                    return render(request,"Guest/Login.html",{"msg2":msg2})
          elif admincount > 0:
               admin = tbl_admin.objects.get(admin_email=email,admin_password=password)
               request.session["aid"] = admin.id
               return redirect("Admin:Adminhome")
          else:
               return render(request, 'Guest/Login.html',{"msg":"Invalid Email or Password"})
     else:
               return render(request, 'Guest/Login.html')    

def Userreg(request):
        
        dis =tbl_district.objects.all()
        if request.method == "POST":
          tbl_user.objects.create(user_name=request.POST.get("name"),
                                  user_email=request.POST.get("email"),
                                  user_contact=request.POST.get("contact"),
                                  user_address=request.POST.get("address"),
                                  user_password=request.POST.get("password"),
                                  user_photo=request.FILES.get("photo"),
                                  user_resume=request.FILES.get("resume"),
                                 place=tbl_place.objects.get(id=request.POST.get("place")))
          return redirect("Guest:Login")
        else:
             return render(request,'Guest/UserRegistration.html',{"district":dis})

def ajaxplace(request):
        place = tbl_place.objects.filter(district=request.GET.get("did"))
        return render(request,'Guest/AjaxPlace.html',{"place":place})


def MyProfile(request):
     return render(request,'User/MyProfile.html')


def Company(request):
      dis =tbl_district.objects.all()
      ctype=tbl_companytype.objects.all()
      if request.method == "POST":
          tbl_company.objects.create(company_name=request.POST.get("cname"),
                                  company_email=request.POST.get("email"),
                                  company_contact=request.POST.get("contact"),
                                  company_address=request.POST.get("address"),
                                  company_password=request.POST.get("password"),
                                  company_logo=request.FILES.get("logo"),
                                  company_licence=request.FILES.get("licence"),
                                  place=tbl_place.objects.get(id=request.POST.get("place")),
                                  companytype=tbl_companytype.objects.get(id=request.POST.get("ctlist")))
          return redirect("Guest:Login")
      else:
             return render(request,'Guest/Company.html',{"district":dis,"cytype":ctype})
      



     