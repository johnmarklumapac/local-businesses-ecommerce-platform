from django.urls import path
from . import views

app_name = 'pasundayag'

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('ipcr-list', views.ipcr_all, name='ipcr-list'),
    path('rate-personnel/<personnel_id>-<int:year>-<str:period>/', views.rate_personnel, name='rate-personnel'),
    path('ipcr-detail/<personnel_id>-<int:year>-<str:period>/', views.ipcr_detail, name='ipcr-detail'),
    path('rank-list/<slug:rank_slug/', views.rank_list, name='rank-list'),
    path('logout',views.logoutuser, name='logout'),

]
