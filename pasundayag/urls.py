from django.urls import path

from . import views

app_name = "pasundayag"

urlpatterns = [
    path("home/", views.pasundayag, name="pasundayag_home"),
]
