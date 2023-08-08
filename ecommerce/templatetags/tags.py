from django import template
from django.contrib.sessions.models import Session

from datetime import datetime, timedelta


register = template.Library()

@register.simple_tag
def generate_session_id():
    expire_date = datetime.now() + timedelta(days=1)
    session = Session.objects.create(expire_date=expire_date)
    return session.session_key