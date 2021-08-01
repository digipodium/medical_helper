from django.urls import path,include
from .views import dashboard_view,register_user

from app.views import *
urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register/',register_user, name='register'),
    path('oauth/',include('social_django.urls')),
   
    

    
   
]