from django.urls import path
from .views import UpdateInfoView
from . import views

app_name = "pasundayag"

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("dashboard/<int:year>", views.index_02, name="dashboard"),
    path("dashboard/<int:year>-<str:rating>", views.index_03, name="dashboard-rating"),
    path("ipcr-list", views.ipcr_all, name="ipcr-list"),
    path("personnel-ipcr-list/<personnel_id>", views.ipcr_per_personnel, name="personnel-ipcr-list"),
    path("academic-title-list", views.academic_title, name="academic-title-list"),
    path("personnel-list/<slug:slug>", views.personnel_per_title, name="personnel-list"),
    path("rate-personnel/<personnel_id>-<int:year>-<str:period>/", views.rate_personnel, name="rate-personnel"),
    path('update-personnel-ipcr/<int:pk>-<int:year>-<str:period>/', UpdateInfoView.as_view(), name='update-personnel-ipcr'),
    path(
        "ipcr-detail-rating/<personnel_id>-<int:year>-<str:period>/",
        views.ipcr_detail_rating,
        name="ipcr-detail-rating",
    ),
    path("ipcr-detail-analytics/<personnel_id>/", views.ipcr_detail_analytics, name="ipcr-detail-analytics"),
    path("rank-list/<slug:slug>/", views.rank_list, name="rank-list"),
    path("logout", views.logoutuser, name="logout"),
]
