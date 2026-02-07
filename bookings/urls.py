from django.urls import path
from . import views

urlpatterns = [
    path('book/<slug:package_slug>/', views.booking_create, name='booking_create'),
    path('success/<str:booking_id>/', views.booking_success, name='booking_success'),
    path('contact/', views.contact_create, name='contact_submit'),
]
