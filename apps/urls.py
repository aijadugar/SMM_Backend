from django.urls import path
from . import views

urlpatterns = [
    path('student/<str:roll_number>/', views.get_student, name='get_student'),
]
