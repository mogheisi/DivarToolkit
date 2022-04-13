from django.shortcuts import render
from unidecode import unidecode
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import re
from sklearn import tree

from .models import *


def daily_price(request):
    if request.method == 'GET':
        DailyPrice.objects.all().delete()
        r = requests.get('https://divar.ir/goods/mobile/prices')
        soup = BeautifulSoup(r.text, "html.parser")
        val = soup.find_all("div", attrs={"class": "kt-price-row kt-price-row--has-icon-button"})
        for v in val:

            # brand = v.find("h2", attrs={"class": "kt-section-title__title"})
            name = v.find("h3", attrs={"class": "kt-price-row__text kt-price-row__title"})
            detail = v.find("p", attrs={"class": "kt-price-row__text kt-price-row__subtitle"})
            price = v.find("p", attrs={"class": "kt-price-row__text kt-price-row__value"})
            changes = v.find("p", attrs={"class": "kt-price-row__text kt-price-row__change kt-price-row__change--increased"})

            context: dict = {
                'name': name.text,
                'detail': detail.text,
                'price': price.text,
            }

            if changes:
                context['changes'] = changes.text

            DailyPrice.objects.create(**context)
        car_r = requests.get('https://divar.ir/car/prices')
        car_soup = BeautifulSoup(car_r.text, 'html.parser')
        date = car_soup.find("h1", attrs={"class": "kt-section-title__title"}).text
        mobile_date = re.sub(r'خودرو', 'موبایل', date)
        return render(request, 'mobile/daily_price.html', {'daily_price': DailyPrice.objects.all(), 'date': mobile_date})
