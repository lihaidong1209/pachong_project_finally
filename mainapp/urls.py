from django.contrib import admin
from django.urls import path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [

    path('admin/', admin.site.urls),
    path('introduce/', views.introduce, name='introduce'),
    path('main/', views.main, name='main'),
    path('menu/', views.menu, name='menu'),

]