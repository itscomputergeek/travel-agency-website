from django.urls import path
from . import views

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('<slug:slug>/', views.package_detail, name='package_detail'),
]
