from django.conf import settings

import requests
import base64
import json
import logging


def get_token_epayco():
    public_key = settings.PUBLIC_KEY
    private_key = settings.PRIVATE_KEY
    logging.warning("cadenas: ")
    logging.warning(public_key)
    logging.warning(private_key)
    credentials = f"{public_key}:{private_key}"
    logging.warning(credentials)
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    session = requests.Session()
    session.headers.update({'Authorization': 'Basic ' + encoded_credentials, 'Content-Type': 'application/json'})
    session.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})
    try:
        r = session.post('https://apify.epayco.co/login', data='')
        if r.status_code == 200:
            return r.json()['token']
    except requests.exceptions.RequestException as e:
        logging.error('Error get token', e)
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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip