from django.urls import path,include

from . import views

app_name = "pages"

urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('contas/',include('contas.urls'),name="user")
]