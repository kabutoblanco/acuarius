from django.conf import settings

import requests
import base64
import json


def get_token_epayco():
    public_key = settings.PUBLIC_KEY
    private_key = settings.PRIVATE_KEY
    credentials = f"{public_key}:{private_key}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    session = requests.Session()
    session.headers.update({'Authorization': 'Basic ' + encoded_credentials, 'Content-Type': 'application/json'})
    r = session.post('https://apify.epayco.co/login', data='')
    if r.status_code == 200:
        return r.json()['token']
    return None


def payment_pse(token, payload):
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    r = session.post('https://apify.epayco.co/payment/process/pse', data=json.dumps(payload))
    if r.status_code == 200:
        return r.json()
    return None


def get_banks(token):
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    r = session.get('https://apify.epayco.co/payment/pse/banks')
    if r.status_code == 200:
        return r.json()
    return {"data": [{"bankCode": "0", "bankName":"A continuaci\ón seleccione su banco"}]}


def get_status_payment(token, payload):
    session = requests.Session()
    session.headers.update({'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'})
    r = session.post('https://apify.epayco.co/transaction/detail', data=json.dumps(payload))
    if r.status_code == 200:
        return r.json()
    return {"data": None}


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip