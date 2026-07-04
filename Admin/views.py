from django.shortcuts import render,redirect
from User.models import *
from Guest.models import *
from Company.models import *
from django.conf import settings
from django.core.mail import send_mail
from datetime import date
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.db.models import Sum
# Create your views here.


def logout(request):
    del request.session['aid']
    return redirect('Guest:Login')


def add(request):
    if request.method=='POST':
        num1=int(request.POST.get('fnumber'))
        num2=int(request.POST.get('snumber'))
        result=num1+num2
        return render(request, 'Admin/add.html',{'res':result})
    else:
        return render(request, 'Admin/add.html')

def largest(request):
    if request.method=='POST':
        num1=int(request.POST.get('fnumber'))
        num2=int(request.POST.get('snumber'))
        if num1>num2:
            result=num1
        else:
            result=num2

        return render(request, 'Admin/largest.html',{'res':result})
    else:
        return render(request, 'Admin/largest.html')
    

def calculator(request):
    if request.method=='POST':
        num1=int(request.POST.get('fnumber'))
        num2=int(request.POST.get('snumber'))
        button=request.POST.get('check')
        if button=='+':
            result=num1+num2
        elif button=='-':
            result=num1-num2
        elif button=='/':
            result=num1/num2
        elif button=='*':
            result=num1*num2
        return render(request, 'Admin/calculator.html',{'res':result})
    else:
        return render(request, 'Admin/calculator.html')
    

def Register(request):
    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        name=fname+" "+lname
        gender=request.POST.get('gender')
        address=request.POST.get('address')
        contact=request.POST.get('contact')
        district=request.POST.get('ddlDist')
        return render(request, 'Admin/Register.html',{'name':name,'gender':gender,'address':address,'contact':contact,'district':district})
    else:
        return render(request, 'Admin/Register.html')
    

def District(request):
    dis=tbl_district.objects.all()
    if request.method=='POST':
        distirct=request.POST.get('district')
        tbl_district.objects.create(
        district_name=distirct
        )
        return render(request,'Admin/District.html',{'msg':"Data Inserted Succesfully"})
    else:
        return render(request,'Admin/District.html',{'district':dis})
    

def editdistrict(request, id):
    district = tbl_district.objects.get(id=id)
    if request.method=="POST":
        district.district_name = request.POST.get("District")
        district.save()
        return redirect("Admin:District")
    else:
        return render(request, 'Admin/District.html',{"disdata":district})


    
def category(request):
    cat=tbl_category.objects.all()
    if request.method=='POST':
        category=request.POST.get('category')
        tbl_category.objects.create(
            category_name=category
        )
        return render(request,'Admin/category.html',{'msg':"Category Added Successfully"})
    else:
        return render(request,'Admin/category.html',{'category':cat})

    

def delcategory(request,id):
    tbl_category.objects.get(id=id).delete()
    return redirect('Admin:category')

def deldistrict(request,id):
    tbl_district.objects.get(id=id).delete()
    return redirect('Admin:District')


def admin(request):
    dis=tbl_admin.objects.all()
    if request.method=='POST':
        a_name=request.POST.get('name')
        a_email=request.POST.get('email')
        a_password=request.POST.get('Password')
        tbl_admin.objects.create(
            admin_name=a_name,
            admin_email=a_email,
            admin_password=a_password
        )
        return render(request,'Admin/adminreg.html',{'msg':"Admin Added Succesfully",'admin':dis})
    else:
        return render(request,'Admin/adminreg.html',{'admin':dis})


def deladmin(request,id):
    tbl_admin.objects.get(id=id).delete()
    return redirect('Admin:admin')    

def editcategory(request, id):
    category = tbl_category.objects.get(id=id)
    if request.method=="POST":
        category.category_name = request.POST.get("category")
        category.save()
        return redirect("Admin:category")
    else:
        return render(request, 'Admin/category.html',{"catdata":category})




def editadmin(request, id):
    if 'aid' in request.session:
        adminreg= tbl_admin.objects.get(id=id)
        if request.method=="POST":
            adminreg.admin_name = request.POST.get("name")
            adminreg.admin_email = request.POST.get("email")
            adminreg.admin_password = request.POST.get("Password")
            adminreg.save()
            return redirect("Admin:admin")
        else:
            return render(request, 'Admin/adminreg.html',{"admindata":adminreg})
    else:
        return redirect('Guest:Login')
        
    
def place(request):
    place= tbl_place.objects.all()
    dist=tbl_district.objects.all()
    if request.method=="POST":
         district=tbl_district.objects.get(id=request.POST.get("ddlDist"))
         tbl_place.objects.create(place_name=request.POST.get("place"),
                                  district=district)
         return redirect('Admin:place')
    else:
        return render(request, 'Admin/place.html',{'district':dist,'place':place})
    
def delplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return redirect('Admin:place')

def editplace(request, id):
    dist = tbl_district.objects.all()
    place = tbl_place.objects.get(id=id)
    if request.method=="POST":
        place.district = tbl_district.objects.get(id=request.POST.get("ddlDist"))
        place.place_name = request.POST.get("place")
        place.save()
        return redirect("Admin:place")
    else:
        return render(request, 'Admin/place.html',{"district":dist,"placdata":place})
    

def subcategory(request):
    subcategory= tbl_subcategory.objects.all()
    category=tbl_category.objects.all()
    if request.method=="POST":
         category=tbl_category.objects.get(id=request.POST.get("subcategory"))
         tbl_subcategory.objects.create(subcategory_name=request.POST.get("subcat"),
                                  category=category)
         return redirect('Admin:subcategory')
    else:
        return render(request, 'Admin/subcategory.html',{'category':category,'subcategory':subcategory})
    

def delsubcategory(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect('Admin:subcategory')


def editsubcategory(request, id):
    category=tbl_category.objects.all()
    subcategory = tbl_subcategory.objects.get(id=id)
    if request.method=="POST":
        subcategory.category =tbl_category.objects.get(id=request.POST.get("subcategory"))
        subcategory.subcategory_name = request.POST.get("subcat")
        subcategory.save()
        return redirect("Admin:subcategory")
    else:
        return render(request, 'Admin/subcategory.html',{'category':category,"subdata":subcategory})
    

def UserVerification(request):
    if 'aid' in request.session:
        user=tbl_user.objects.all()
        return render(request,'Admin/UserVerification.html',{'user':user})
    else:
        return redirect('Guest:Login')

    
def userreject(request,id):
    user = tbl_user.objects.get(id=id)
    user.user_status = 1
    user.save()
    return redirect("Admin:UserVerification")

def Product(request):
             category=tbl_category.objects.all()
             Product=tbl_product.objects.all()
             if request.method=="POST":
                 tbl_product.objects.create(product_name=request.POST.get("pname"),
                                price=request.POST.get("price"),
                                details=request.POST.get("details"),
                                product_photo=request.FILES.get("photo"),
                                subcategory=tbl_subcategory.objects.get(id=request.POST.get("subcat")))
                 return redirect("Admin:Product")
             
             else: 
                 return render(request,'Admin/Product.html',{"category":category,"Product":Product})
        


def ajaxcategory(request):
        subcategory = tbl_subcategory.objects.filter(category=request.GET.get("did"))
        return render(request,'Admin/ajaxcategory.html',{"subcategory":subcategory})

def Companytype(request):
    if 'aid' in request.session:
        company=tbl_companytype.objects.all()
        if request.method=="POST":
            tbl_companytype.objects.create(company_type=request.POST.get("ctype"))
            return redirect("Admin:Companytype")
        else:
            return render(request,'Admin/Companytype.html',{'company':company})
    
def delcompanytype(request,id):
    tbl_companytype.objects.get(id=id).delete()
    return redirect('Admin:Companytype')

def Viewcompany(request):
     if 'aid' in request.session:
         company=tbl_company.objects.filter(company_status=0)
         return render(request,'Admin/Viewcompany.html',{"company":company})
     else:
         return redirect('Guest:Login')

def companyaccept(request,id):
    company = tbl_company.objects.get(id=id)
    company.company_status = 1
    company.save()
    return redirect("Admin:Acceptedcompany")

def companyreject(request,id):
    company = tbl_company.objects.get(id=id)
    company.company_status = 2
    company.save()
    return redirect("Admin:Rejectedcompany")

def Acceptedcompany(request):
    if 'aid' in request.session:
        company=tbl_company.objects.filter(company_status='1')
        return render(request,'Admin/Acceptedcompany.html',{'company':company})
    else:
        return redirect('Guest:Login')

def Rejectedcompany(request):
    if 'aid' in request.session:
        company=tbl_company.objects.filter(company_status='2')
        return render(request,'Admin/Rejectedcompany.html',{'company':company})
    else:
        return redirect('Guest:Login')
    
from django.http import JsonResponse

def get_chart_data (request):
    data = {
        "labels": ["Jan", "Feb", "Mar"],
        "values": [100, 200, 300]
    }
    return JsonResponse(data)


def Adminhome(request):
    # Dashboard statistics
    today = date.today()
    admin=tbl_admin.objects.get(id=request.session['aid'])
    totalsubscriptions = tbl_payment.objects.filter(payment_status=0).count()
    totalusers = tbl_user.objects.count()
    acceptedusers=tbl_user.objects.filter(user_status=0).count()
    rejectedusers=tbl_user.objects.filter(user_status=1).count()
    acceptedcompany=tbl_company.objects.filter(company_status=1).count()
    rejectedcompany=tbl_company.objects.filter(company_status=2).count()
    totaljobs=tbl_job.objects.count()
    activejobs=tbl_job.objects.filter(job_lastdate__gte=today).count()
    expiredjobs=tbl_job.objects.filter(job_lastdate__lt=today).count()
    totalcompanys = tbl_company.objects.count()
    totalamount=tbl_payment.objects.count()
    subprice=500
    monthrevenue=totalsubscriptions*subprice
    totalearning=totalamount*subprice

    context = {
        'admin':admin,
        'acceptedusers':acceptedusers,
        'rejectedusers':rejectedusers,
        'acceptedcompany':acceptedcompany,
        'rejectedcompany':rejectedcompany,
        'totalearning':totalearning,
        'monthrevenue':monthrevenue,
        'totalsubscriptions': totalsubscriptions,
        'totalusers': totalusers,
        'totalcompanys': totalcompanys,
        'totaljobs':totaljobs,
        'activejobs':activejobs,
        'expiredjobs':expiredjobs,
    }

    return render(request, 'Admin/Adminhome.html', context)

def Jobtype(request):
    if 'aid' in request.session:
        job=tbl_jobtype.objects.all()
        if request.method=="POST":
            tbl_jobtype.objects.create(job_type=request.POST.get("jtype"))
            return redirect("Admin:Jobtype")
        else:
            return render(request,'Admin/Jobtype.html',{'job':job})
    else:
        return redirect('Guest:Login')
    
def Jobgroup(request):
    if 'aid' in request.session:
        job=tbl_jobgroup.objects.all()
        if request.method=="POST":
            tbl_jobgroup.objects.create(job_group=request.POST.get("jgroup"))
            return redirect("Admin:Jobgroup")
        else:
            return render(request,'Admin/Jobgroup.html',{'job':job})
    else:
        return redirect('Guest:Login')
    
def deljobtype(request,id):
    tbl_jobtype.objects.get(id=id).delete()
    return redirect('Admin:Jobtype')

def Materials(request):
    if 'aid' in request.session:
        materials=tbl_materials.objects.all()
        Jobgroup=tbl_jobgroup.objects.all()
        if request.method=='POST':
            tbl_materials.objects.create(jobgroup=tbl_jobgroup.objects.get(id=request.POST.get("jbglist")),
                                     material_file=request.FILES.get("Material"))
            return redirect("Admin:Materials")
        else:
            return render(request,'Admin/Materials.html',{'jobgroup':Jobgroup,'materials':materials})
    else:
        return redirect('Guest:Login')
    
def delmaterial(request,id):
    tbl_materials.objects.get(id=id).delete()
    return redirect('Admin:Materials')

def Viewfeedback(request):
     if 'aid' in request.session:
         feedback=tbl_feedback.objects.all()
         return render(request,'Admin/Viewfeedback.html',{"feedback":feedback})
     else:
         return redirect('Guest:Login')

def Viewcomplaint(request):
     if 'aid' in request.session:
        user=tbl_user.objects.all()
        company=tbl_company.objects.all()
        ucomplaint=tbl_complaints.objects.filter(user__in=user,complaint_status=0)
        ccomplaint=tbl_complaints.objects.filter(Company__in=company,complaint_status=0)
        return render(request,'Admin/Viewcomplaints.html',{"ucomplaint":ucomplaint,"ccomplaint":ccomplaint})
     else:
         return redirect('Guest:Login')

def replay(request,id):
    replay=tbl_complaints.objects.get(id=id)
    if request.method=="POST":
        replay.complaint_replay=request.POST.get("replay")
        replay.complaint_status=1
        replay.save()
        return redirect("Admin:Rcomplaint")
    else:
        return render(request,'Admin/replay.html')
    
def Rcomplaint(request):
     if 'aid' in request.session:
         user=tbl_user.objects.all()
         company=tbl_company.objects.all()
         ucomplaint=tbl_complaints.objects.filter(user__in=user,complaint_status=1)
         ccomplaint=tbl_complaints.objects.filter(Company__in=company,complaint_status=1)
         return render(request,'Admin/Rcomplaint.html',{"ucomplaint":ucomplaint,"ccomplaint":ccomplaint})
     else:
         return redirect('Guest:Login')
    
def subpeople(request):
    data = tbl_payment.objects.all()
    return render(request,"Admin/Subscribed_people.html",{"data":data})


def Header(request):
    if 'aid' not in request.session:
        admin=tbl_admin.objects.get(id=request.session['aid'])
        return redirect('login',{"admin":admin})  # Redirect to login if session is missing

    admin = tbl_admin.objects.get(id=request.session['aid'])
    return render(request, "Admin/Header.html", {'admin': admin})


def Rejectcompany(request, id):
    req = tbl_company.objects.get(id=id)
    company_email = req.company_email
    name = req.company_name

    if request.method == "POST":
        title = request.POST.get('subject')
        content = request.POST.get('content')
        req.company_status = 2
        req.save()

        email_subject = title
        email_message = f"Dear {name},\n\n{content}\n\nBest regards,\nWork Elite"

        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[company_email],
        )

        return redirect('Admin:Rejectedcompany')
    
    return render(request, "Admin/Rejectcompany.html")

def adminreport(request):
    if "start_date" not in request.GET or "end_date" not in request.GET:
        return render(request, "Admin/adminreport.html")

    start_date = parse_date(request.GET.get("start_date"))
    end_date = parse_date(request.GET.get("end_date"))

    if not start_date or not end_date:
        return JsonResponse({"error": "Invalid date range"}, status=400)

    users_joined = list(tbl_user.objects.filter(created_at__range=[start_date, end_date])
                         .values("user_name", "created_at"))
    
    formatted_users = [{"name": user["user_name"], "joined_at": user["created_at"], "role": "User"} for user in users_joined]

    companies_joined = list(tbl_company.objects.filter(created_at__range=[start_date, end_date])
                            .values("company_name", "created_at"))

    formatted_companies = [{"name": company["company_name"], "joined_at": company["created_at"], "role": "Company"} for company in companies_joined]

    total_subscriptions = tbl_payment.objects.filter(payment_date__range=[start_date, end_date]).count()
    total_revenue = total_subscriptions * 500

    payments = (
        tbl_payment.objects
        .values("user__user_name")  # Get total subscriptions for each user
        .annotate(subscription_count=models.Count("id"))  # Count total subscriptions
            )

    # Fetch only first payment date within the selected range
    filtered_payments = (
        tbl_payment.objects.filter(payment_date__range=[start_date, end_date])
        .values("user__user_name")
        .annotate(first_payment=models.Min("payment_date"))  # Get first payment date in range
    )

    # Convert filtered payments into a dictionary for easy lookup
    payment_dates = {p["user__user_name"]: p["first_payment"] for p in filtered_payments}

    formatted_payments = [
        {
            "username": payment["user__user_name"],
            "payment_date": payment_dates.get(payment["user__user_name"], "N/A"),  # Get first payment date in range
            "subscriptions_taken": payment["subscription_count"]  # Total subscriptions taken by user
        }
        for payment in payments
    ]

    return JsonResponse({
        "users_joined": formatted_users, 
        "companies_joined": formatted_companies,
        "total_subscriptions": total_subscriptions,
        "total_revenue": total_revenue,
        "payments": formatted_payments
    })
