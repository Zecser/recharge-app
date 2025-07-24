from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.plans_list, name='plans_list'),
    path('plans<int:pk>/', views.plans_detail, name='plans_detail'),
    path('providers/', views.providers_list, name='providers_list'),
]