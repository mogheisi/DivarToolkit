from asgiref.sync import sync_to_async
from django.shortcuts import render
from unidecode import unidecode
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import re
from sklearn import tree

from .models import *
from .forms import *


def index(request):
    return render(request, 'index.html')


def scraping(request):
    global searches
    if request.method == 'GET':
        form = CarCounter()
        return render(request, 'car/car.html', {'form': form})
    if request.method == 'POST':
        form = CarCounter(request.POST)
        if form.is_valid():
            searches = form.cleaned_data['count']
        r = requests.get('https://divar.ir/s/iran/auto')
        soup = BeautifulSoup(r.text, 'html.parser')
    
        val = soup.find_all('div', attrs={'class': 'post-card-item kt-col-6 kt-col-xxl-4'})
        count = 0
        while count < searches:
            for v in val:
                next_page = re.findall(r'href=\"(.*)\"><div class=\"kt-post-card__b', str(v))
                check = re.search(r'تومان', str(v.text))

                if check:
                    req = requests.get(f'https://divar.ir{next_page[0]}')
                    r = re.sub('\u200c', ' ', req.text)
                    check_name = re.search(r'<title data-react-helmet=\"true\">(.*?)،', r)
                    check_kilometers = re.search(
                        r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">کارکرد</span><span class=\"kt-group-row-item__value\">(.*?)</span>',
                        r)
                    check_model = re.search(
                        r'</span><span class=\"kt-group-row-item__value\">(\d*)</span></div><div class=\"kt-group-row-item kt-group-row-item--info-row\"><span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span>',
                        r)
                    check_color = re.search(
                        r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span><span class=\"kt-group-row-item__value\">(.*?)</span>',
                        r)
                    name = re.findall(
                        r'<h1 class=\"kt-page-title__title kt-page-title__title--responsive-sized\">(.*)</h1>', r)
                    if check_name and check_kilometers and check_model and check_color:
                        count += 1
                        kilometers = re.findall(
                            r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">کارکرد</span><span class=\"kt-group-row-item__value\">(.*?)</span>',
                            r)
                        model = re.findall(
                            r'</span><span class=\"kt-group-row-item__value\">(\d*)</span></div><div class=\"kt-group-row-item kt-group-row-item--info-row\"><span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span>',
                            r)
                        price = re.findall(r'\d+٬\d+٬\d+', r)
                        color = re.findall(
                            r'<span class=\"kt-group-row-item__title kt-body kt-body--sm\">رنگ</span><span class=\"kt-group-row-item__value\">(.*?)</span>',
                            r)
                        new_price = re.sub(',', '.', unidecode(price[0]))
                        new_kilometer = re.sub(',', '.', unidecode(kilometers[0]))
                        link = re.findall(r'href=\"(.*?)\"', str(v))  # href=\"(.*)\">#
                        Car.objects.create(name=name[0], price=new_price, kilometer=new_kilometer, model=unidecode(model[0]), color=color[-1], link=f"https://divar.ir{link[0]}")
            if count == searches:

                return render(request, 'car/done.html', {'searches': searches})


def show(request):
    if request.method == 'GET':
        cars = Car.objects.all()
        return render(request, 'car/show.html', {'cars': cars})


def predict(request):
    if request.method == 'GET':
        form = CarForm()
        return render(request, 'car/predict.html', {'form': form})
    if request.method == 'POST':
        form = CarForm(request.POST)
        x = []
        y = []
        if form.is_valid():
            for line in Car.objects.all():
                found = re.search(form.cleaned_data['name'], line.name)
                if found:
                    x.append((line.model, line.kilometer))
                    y.append(line.price)

            clf = tree.DecisionTreeClassifier()
            clf.fit(x, y)

            model = form.cleaned_data['model']
            kilometers = form.cleaned_data['kilometers']

            new_data = [[kilometers, model]]
            answer = clf.predict(new_data)
            return render(request, 'car/result.html', {'answer': answer[0]})


def daily_price(request):
    if request.method == 'GET':
        DailyPrice.objects.all().delete()
        r = requests.get('https://divar.ir/car/prices')
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
        date = soup.find("h1", attrs={"class": "kt-section-title__title"}).text
        return render(request, 'car/daily_price.html', {'daily_price': DailyPrice.objects.all(), 'date': date})

