from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'), 
    path('sum/<int:num1>/<int:num2>', views.sum, name='sum')
]
