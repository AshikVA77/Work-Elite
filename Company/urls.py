from django.urls import path
from Company import views
app_name="Company"
urlpatterns = [
 path('Companyhome/',views.Companyhome,name='Companyhome'),
 path('Companyprofile/',views.Companyprofile,name='Companyprofile'),
 path('editcprofile/',views.editcprofile,name='editcprofile'),
 path('ChangePassword/',views.ChangePassword,name='ChangePassword'),
 path('Addjob/',views.Addjob,name='Addjob'),
 path('deljob/<int:id>',views.deljob,name='deljob'),
 path('ViewApplicants/<int:id>',views.ViewApplicants,name='ViewApplicants'),
 path('rejectapplicant/<int:id>',views.rejectapplicant,name='rejectapplicant'),
 path('Sendmail/<int:id>',views.Sendmail,name='Sendmail'),
 path('Ccomplaint/',views.Ccomplaint,name='Ccomplaint'),
 path('interviewlink/',views.interviewlink,name='interviewlink'),
 path('delcomplaint/<int:id>',views.delcomplaint,name='delcomplaint'),
 path('about/',views.about,name='about'),
 path('logout/',views.logout,name='logout'),
]