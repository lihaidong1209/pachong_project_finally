from django.contrib import admin
from django.urls import path
from userapp import views

app_name = 'userapp'

urlpatterns = [

    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('name/', views.name, name='name'),
    path('isPhone/', views.isPhone, name='isPhone'),
    path('isEmail/', views.isEmail, name='isEmail'),
    path('pwd/', views.pwd, name='pwd'),
    path('message/', views.message, name='message'),
    path('checkcode/', views.checkcode, name='checkcode'),
    path('registerlogic/', views.registerlogic, name='registerlogic'),
    path('login/', views.login, name='login'),
    path('loginlogic/', views.loginlogic, name='loginlogic'),

]

