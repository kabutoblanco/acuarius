from django import forms

from .models import Order, Payment

import datetime


class OrderForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_schedule = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise forms.ValidationError('La dirección debe tener al menos 10 caracteres.')
        return address

    def clean_date_schedule(self):
        date_schedule = self.cleaned_data.get('date_schedule')
        diff = (date_schedule.astimezone(datetime.timezone.utc) - datetime.datetime.now(tz=datetime.timezone.utc)).total_seconds() / 60
        if diff < 45:
            raise forms.ValidationError('El tiempo de entrega debe ser mayor a 45 minutos.')
        return date_schedule

    class Meta:
        model = Order
        fields = ['is_pickup', 'address', 'date_schedule']


class PaymentForm(forms.ModelForm):
    num_document = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cellphone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}'}))

    def clean_num_document(self):
        num_document = self.cleaned_data.get('num_document')
        if not (len(num_document) == 8 or len(num_document) == 10):
            raise forms.ValidationError('Longitud del número de documento invalida.')
        return num_document

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 10:
            raise forms.ValidationError('La dirección debe tener al menos 10 caracteres.')
        return address

    def clean_cellphone(self):
        cellphone = self.cleaned_data.get('cellphone')
        if len(cellphone) != 10:
            raise forms.ValidationError('El celular debe tener 10 números.')
        return cellphone

    class Meta:
        model = Payment
        fields = ['num_document', 'first_name', 'last_name', 'email', 'address', 'cellphone']