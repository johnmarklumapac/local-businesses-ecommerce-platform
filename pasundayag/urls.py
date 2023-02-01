from django.urls import path

from . import views

app_name = "pasundayag"

urlpatterns = [
    path("pasundayag_home/", views.pasundayag_home, name="pasundayag_home"),
]
