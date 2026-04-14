from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/submit/', views.submit, name='submit'),
    path('profile/<str:employee_id>/', views.profile, name='profile'),
    path('api/update/<str:employee_id>/', views.update_employee, name='update_employee'),
    path('api/regenerate/<str:employee_id>/', views.regenerate_badge, name='regenerate_badge'),
]
