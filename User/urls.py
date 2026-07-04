from django.urls import path
from User import views
app_name="User"
urlpatterns = [
    path('Homepage/',views.Homepage,name='Homepage'),
    path('Header/',views.Header,name='Header'),
    path('MyProfile/',views.MyProfile,name='MyProfile'),
    path('Editprofile/',views.Editprofile,name='EditProfile'),
    path('ChangePassword/',views.ChangePassword,name='ChangePassword'),
    path('Viewjob/',views.Viewjob,name='Viewjob'),
    path('Addrequest/<int:id>',views.Addrequest,name='Addrequest'),
    path('Myapplications/',views.Myapplications,name='Myapplications'),
    path('Feedback/',views.Feedback,name='Feedback'),
    path('Complaint/',views.Complaint,name='Complaint'),
    path('delcomplaint/<int:id>',views.delcomplaint,name='delcomplaint'),
    path('ViewCompany/<int:id>',views.ViewCompany,name='ViewCompany'),
    path('viewcjob/<int:id>', views.Viewcjob, name='Viewcjob'),
    path('companysprofile/', views.companysprofile, name='companysprofile'),
    path('Viewmaterials/',views.Viewmaterials,name='Viewmaterials'),
    path('about/',views.about,name='about'),
    path('logout/',views.logout,name='logout'),

    path('Allpayment/',views.Allpayment,name='Allpayment'),
    path('payment/',views.payment,name='payment'),
    path('loader/',views.loader,name='loader'),
    path('paymentsuc/',views.paymentsuc,name='paymentsuc'),

    path('ajaxchecksubscription/',views.ajaxchecksubscription,name='ajaxchecksubscription'),

    path('rating/<int:mid>',views.rating,name="rating"),  
    path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
    path('starrating/',views.starrating,name="starrating"),

]