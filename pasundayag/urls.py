from django.urls import path

from . import views

app_name = "pasundayag"

urlpatterns = [
    path("", views.product_all, name="pasundayag_home"),
    path("<slug:slug>", views.product_detail, name="product_detail"),
    path("shop/<slug:rank_slug>/", views.rank_list, name="rank_list"),
]
