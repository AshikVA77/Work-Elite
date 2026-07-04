from django.urls import path
from Guest import views
app_name="Guest"
urlpatterns = [
    path('Login/',views.Login,name='Login'),
    path('UserRegistration/',views.Userreg,name='UserRegistrstion'),
    path('AjaxPlace/',views.ajaxplace,name='ajaxplace'),
    path('Company/',views.Company,name='Company'),
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    
    

]