from django import forms


class CarCounter(forms.Form):
    count = forms.IntegerField(label='count', min_value=1)


class CarForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    model = forms.CharField(label='model', max_length=100)
    kilometers = forms.CharField(label='kilometers', max_length=100)
