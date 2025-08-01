from django.urls import path
from . import views
from .views import update_provider_discount

urlpatterns = [
    path('', views.plans_list, name='plans_list'),
    path('<int:pk>/', views.plans_detail, name='plans_detail'),
    path('providers/', views.providers_list, name='providers_list'),
    path('provider/<int:id>/set-discount/', update_provider_discount, name='update-provider-discount'),
]