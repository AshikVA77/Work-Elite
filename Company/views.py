from django.shortcuts import render,redirect
from Company.models import *
from Guest.models import *
from Admin.models import *
from User.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.
def logout(request):
    del request.session['cid']
    return redirect('Guest:index')

def Companyhome(request):
    company=tbl_company.objects.get(id=request.session['cid'])
    if 'cid' in request.session:
         return render(request,'Company/Companyhome.html',{'company':company})
    else:
         return redirect("Guest:Login")
    
def Companyprofile(request):
     if 'cid' in request.session:
          company=tbl_company.objects.get(id=request.session['cid'])
          return render(request,'company/Companyprofile.html',{'company':company})
     else:
          return redirect('Guest:Login')

def editcprofile(request):
     if 'cid' in request.session:
          company=tbl_company.objects.get(id=request.session['cid'])
          if request.method == "POST":
               company.company_name=request.POST.get("uname")
               company.company_email=request.POST.get("email")
               company.company_contact=request.POST.get("contact")
               company.company_address=request.POST.get("address")
               company.interview_link=request.POST.get("interviewlink")
               company.company_logo = request.FILES.get("logo")
               company.save()
               return redirect("Company:Companyprofile")
          else:
               return render(request,'Company/editcprofile.html',{'company':company})
     else:
          return redirect('Guest:Login')
     
def ChangePassword(request):
     if 'cid' in request.session:
          npassword=request.POST.get('newpassword')
          rpassword=request.POST.get('retypepassword')
          opassword=request.POST.get('oldpassword')
          commpany=tbl_company.objects.get(id=request.session['cid'])
          if request.method=="POST":
               if commpany.company_password == opassword:
                    if npassword==rpassword:
                         commpany.company_password=request.POST.get("newpassword")
                         commpany.save()
                         return redirect("Company:Companyprofile")
                    else:
                         return render(request,'Company/ChangePassword.html',{"msg":"Error in New password"})
               else:
                    return render(request,'Company/ChangePassword.html',{"msg":"Error in Old password"})
          else:
               return render(request,'Company/ChangePassword.html')
     else:
          return redirect('Guest:Login')
     
def Addjob(request):
    if 'cid' in request.session:
        company = tbl_company.objects.get(id=request.session['cid'])
        job = tbl_job.objects.filter(company=request.session['cid'])
        jobgroup = tbl_jobgroup.objects.all()
        jobtype = tbl_jobtype.objects.all()


        if request.method == "POST":
            new_job = tbl_job.objects.create(
                job_title=request.POST.get("title"),
                job_details=request.POST.get("details"),
                job_lastdate=request.POST.get("lastdate"),
                job_qualification=request.POST.get("Qualification"),
                job_salary=request.POST.get("salary"),
                company=company,
                jobgroup=tbl_jobgroup.objects.get(id=request.POST.get("jbtlist")),
                jobtype=tbl_jobtype.objects.get(id=request.POST.get("jbtype"))
            )

            users_with_paystatus = tbl_user.objects.filter(user_paystatus=1)
            subject = "New Jobs Listed"
            for user in users_with_paystatus:
                name = user.user_name
                user_email = user.user_email
                message = (
                    f"Dear {name},\n\n"
                    "We are excited to inform you that new job opportunities have been added by companies. "
                    "Log in to your account to check them out and apply now!\n\n"
                    "Best regards,\nWork Elite"
                )

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email],
                )

            return redirect("Company:Addjob")
        else:
            return render(request, 'Company/Addjob.html', {"job": job, "jobgroup": jobgroup,"jobtype": jobtype})
    else:
        return redirect('Guest:Login')
      

def deljob(request,id):
    tbl_job.objects.get(id=id).delete()
    return redirect('Company:Addjob')

def ViewApplicants(request,id):
     applicants=tbl_request.objects.filter(job_id=id)
     return render(request,'Company/ViewApplicants.html',{'applicants':applicants})

def rejectapplicant(request, id):
    req = tbl_request.objects.get(id=id)
    req.request_status = 2  
    req.save()

    user = req.user  # Directly get user from request
    user_email = user.user_email
    name = user.user_name

    print(f"Sending rejection email to: {user_email}")  # Debugging line

    if not user_email:
        print("Error: Email is empty!")
        return redirect('Company:Addjob')

    subject = "Application Rejected"
    message = f"Dear {name},\n\nWe regret to inform you that your application has been rejected.\n\nBest regards,\nWork Elite"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )

    return redirect('Company:Addjob')



def Sendmail(request, id):
    req = tbl_request.objects.get(id=id)
    userid=req.user.id
    user = tbl_user.objects.get(id=userid)
    user_email = user.user_email
    name=user.user_name

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('Content')

        req.request_status=1
        req.save()

        
        email_subject = title
        email_message = f"Dear {name},\n\n{content}\n\nBest regards,\nWork Elite"

        
        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
        )

        return redirect('Company:Addjob')
    
    else:
        return render(request, 'Company/Sendmail.html')


def Ccomplaint(request):
     complaint=tbl_complaints.objects.filter(Company=request.session['cid'])
     if request.method == "POST":
          tbl_complaints.objects.create(complaint_title=request.POST.get("title"),
                                      complaint_content=request.POST.get("content"),  
                                      Company=tbl_company.objects.get(id=request.session['cid']))
          return redirect('Company:Ccomplaint')
     else:
          return render(request,'Company/Ccomplaint.html',{'complaint':complaint})
     
def delcomplaint(request,id):
    tbl_complaints.objects.get(id=id).delete()
    return redirect('Company:Ccomplaint')

def  about(request):
     return render(request,"Company/about.html")

def  interviewlink(request):
     interview=tbl_company.objects.get(id=request.session['cid'])
     if request.method == "POST":
          interview.interview_link=request.POST.get("interview")
          interview.save()
          return redirect("Company:Companyprofile")
     else:
          return render(request,"Company/interviewlink.html")


