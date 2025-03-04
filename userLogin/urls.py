from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signUp, name='signUp'),
    # path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update')
]
