from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home,name="home"),
    path('customerform',views.createCustomer,name="customerform"),
    path('adminpage',views.adminpage,name="adminpage"),
    path('update/<str:pk>',views.updatecustomer,name="update"),
    path('deletecustomer/<str:pk>',views.deletecustomer,name="deletecustomer"),
    path('login',views.loginuser,name='login'),
    path('register',views.registeruser,name='register'),
    path('logout',views.logoutuser,name='logout'),
    path('dataupload',views.dataupload,name="dataupload"),
    path('formatupload',views.formatUpload,name="formatupload"),
    path('userpage',views.userpage,name="userpage"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
