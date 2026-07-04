from django.shortcuts import render,redirect
from Guest.models import *
from User.models import *
from Company.models import *
from datetime import date
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def logout(request):
    del request.session["uid"]
    return redirect('Guest:index')

def  about(request):
     return render(request,"User/about.html")

def  Header(request):
     user=tbl_user.objects.get(id=request.session['uid'])
     return render(request,"User/about.html",{'user':user})

def Homepage(request):
     user=tbl_user.objects.get(id=request.session['uid'])
     if 'uid' in request.session:
         return render(request,'User/Homepage.html',{'user':user})
     else:
         return redirect("Guest:Login")

def MyProfile(request):
     if 'uid' in request.session:
          user=tbl_user.objects.get(id=request.session['uid'])
          return render(request,'User/MyProfile.html',{'user':user})
     else:
          return redirect("Guest:Login")

def Editprofile(request):
    if 'uid' in request.session:
        user = tbl_user.objects.get(id=request.session['uid'])
        if request.method == "POST":
            user.user_name = request.POST.get("uname")
            user.user_email = request.POST.get("email")
            user.user_contact = request.POST.get("contact")
            user.user_address = request.POST.get("address")
            user.user_photo = request.FILES.get("photo")
            user.save()
            return redirect("User:MyProfile")
        return render(request, 'User/Editprofile.html', {'user': user})
    return redirect("Guest:Login")


def ChangePassword(request):
     if 'uid'in request.session:
          npassword=request.POST.get('newpassword')
          rpassword=request.POST.get('retypepassword')
          opassword=request.POST.get('oldpassword')
          user=tbl_user.objects.get(id=request.session['uid'])
          if request.method=="POST":
               if user.user_password == opassword:
                    if npassword==rpassword:
                         user.user_password=request.POST.get("newpassword")
                         user.save()
                         return redirect("User:MyProfile")
                    else:
                         return render(request,'User/ChangePassword.html',{"msg":"Error in New password"})
               else:
                    return render(request,'User/ChangePassword.html',{"msg":"Error in Old password"})
          else:
               return render(request,'User/ChangePassword.html')
     else:
          return redirect("Guest:Login")

     


def Viewjob(request):
    if 'uid' in request.session:
        search_query = request.GET.get('search', '')
        job_type_filter = request.GET.get('job_type', '')
        jobs = tbl_job.objects.filter(company__company_status=1)

        if job_type_filter == "default":
            job_type_filter = ""

        if search_query:
            jobs = jobs.filter(job_title__icontains=search_query)

        if job_type_filter:
            jobs = jobs.filter(jobtype__job_type__icontains=job_type_filter)

        job_types = tbl_jobtype.objects.all()
        user_id = request.session.get('uid')
        user_applied_jobs = tbl_request.objects.filter(user_id=user_id).values_list('job_id', flat=True)
        return render(request, 'User/Viewjob.html', {
            'job': jobs,
            'search_query': search_query,
            'job_types': job_types,
            'job_type_filter': job_type_filter,
            'today': date.today(),
            'user_applied_jobs': user_applied_jobs
        })
    else:
        return redirect('Guest:Login')


def Addrequest(request,id):
     if 'uid' in request.session:
          tbl_request.objects.create(user=tbl_user.objects.get(id=request.session['uid']),
                                job=tbl_job.objects.get(id=id))
          return redirect('User:Viewjob')
     else:
          return redirect('Guest:Login')
     

def Myapplications(request):
     if 'uid' in request.session:
          job=tbl_request.objects.filter(user_id=request.session['uid'])
          return render(request,'User/Myapplications.html',{'job':job})
     else:
          return redirect("Guest:Login")

def Feedback(request):
     if 'uid' in request.session:
          if request.method == "POST":
               tbl_feedback.objects.create(feedback_content=request.POST.get("feedback"),
                                         user=tbl_user.objects.get(id=request.session['uid']))
               return redirect('User:Feedback')
          else:
               return render(request,'User/Feedback.html')
     else:
          return redirect("Guest:Login")
     

def Complaint(request):
     if 'uid' in request.session:
          complaint=tbl_complaints.objects.filter(user=request.session['uid'])
          if request.method == "POST":
               tbl_complaints.objects.create(complaint_title=request.POST.get("title"),
                                      complaint_content=request.POST.get("content"),  
                                      user=tbl_user.objects.get(id=request.session['uid']))
               return redirect('User:Complaint')
          else:
               return render(request,'User/Complaint.html',{'complaint':complaint})
     else:
          return redirect("Guest:Login")
     
     
def delcomplaint(request,id):
    if 'uid' in request.session:
         tbl_complaints.objects.get(id=id).delete()
         return redirect('User:Complaint')
    else:
         return redirect("Guest:Login")

def payment(request):
    paymentcount = tbl_payment.objects.filter(
        user=request.session["uid"],
        payment_enddate__gt=date.today(),
        payment_status=0
    ).count()

    if paymentcount > 0:
        return render(request, 'User/Payment.html', {'msg': 'You have already paid for the current month'})

    if request.method == 'POST':
        pay_date = date.today()
        exp_date = pay_date + relativedelta(months=1)

        tbl_payment.objects.create(
            payment_enddate=exp_date,
            user=tbl_user.objects.get(id=request.session["uid"])
        )

        user = tbl_user.objects.get(id=request.session["uid"])
        user.user_paystatus = 1
        user.save()

        return redirect('User:loader')

    return render(request, 'User/Payment.html')

def loader(request):
     return render(request,'User/Loader.html')

def paymentsuc(request):
     return render(request,'User/Payment_suc.html')


def ajaxchecksubscription(request):
    count = tbl_payment.objects.filter(
        user=request.session["uid"],
        payment_status=0,
        payment_enddate__lte=date.today()
    ).exists()

    if count:
        tbl_payment.objects.filter(
            user=request.session["uid"],
            payment_status=0,
            payment_enddate__lte=date.today()
        ).update(payment_status=1)

        user = tbl_user.objects.get(id=request.session["uid"])
        user.user_paystatus = 0
        user.save()

        send_mail(
            subject="Subscription Ended",
            message=f"Dear {user.user_name},\n\nYour subscription has ended. Please renew your subscription to continue enjoying our services.\n\nBest regards,\nWork Elite",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.user_email],
        )

        return JsonResponse({"msg": 0})
    return JsonResponse({"msg": 1})

     
def ViewCompany(request,id):
     ar=[1,2,3,4,5]
     parry=[]
     avg=0
     company=tbl_company.objects.get(id=id)
     tot=0
     ratecount=tbl_rating.objects.filter(company=company).count()
     if ratecount>0:
          ratedata=tbl_rating.objects.filter(company=company)
          for j in ratedata:
               tot=tot+j.rating_data
               avg=tot//ratecount
               #print(avg)
          parry.append(avg)
     else:
          parry.append(0)
          # print(parry)
     # datas=zip(company,parry)
     return render(request,'User/ViewCompany.html',{'company':company,'parry':parry,'ar':ar})

def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
   
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(company=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(company=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session['uid']),user_review=user_review,rating_data=rating_data,company=tbl_company.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(company=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(company=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(company=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)


def Viewcjob(request, id):
    company = tbl_company.objects.get(id=id)
    jobs = tbl_job.objects.filter(company=company)

    user_id = request.session.get('uid')
    applied_jobs = []

    if user_id:
        applied_jobs = tbl_request.objects.filter(user_id=user_id, job__in=jobs).values_list('job_id', flat=True)

    return render(request, 'User/Viewcjob.html', {
        'jobs': jobs,
        'company': company,
        'applied_jobs': applied_jobs
    })



def companysprofile(request):
    company_list = tbl_company.objects.filter(company_status=1)
    ar = [1, 2, 3, 4, 5]

    companies = []
    for company in company_list:
        company_rating = tbl_rating.objects.filter(company=company).first()
        rating_value = company_rating.rating_data if company_rating else 0
        companies.append({'company': company, 'rating': rating_value})

    return render(request, 'User/companysprofile.html', {'companies': companies, 'ar': ar})




def Viewmaterials(request):
    if 'uid' in request.session:
        jobgroup = tbl_jobgroup.objects.all()
        materials = []
        error = None

        if request.method == 'POST':
            selected_jobgroup = request.POST.get("jbglist")
            if selected_jobgroup and selected_jobgroup != "---Select---":
                materials = tbl_materials.objects.filter(jobgroup_id=selected_jobgroup)
            else:
                error = "Please select a valid job Group."

        return render(request, 'User/ViewMaterials.html', {'jobgroup': jobgroup, 'materials': materials, 'error': error})
    else:
        return redirect('Guest:Login')



def Allpayment(request):
     return render(request,'User/Allpayment.html')