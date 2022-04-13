from django.urls import path
from . import views

urlpatterns = [
    path('mobile/prices', views.daily_price, name='daily_price'),
]