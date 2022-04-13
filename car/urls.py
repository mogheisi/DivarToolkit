from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('base/', base),
    path('car/', scraping, name='car_list'),
    path('car/show/', show, name='car_show'),
    path('car/predict/', predict, name='car_predict'),
    path('car/prices', daily_price, name='daily_price'),
]
