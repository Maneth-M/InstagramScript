from __future__ import absolute_import, unicode_literals
from celery import task
#imports needed for the functions
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from .models import *
from django.contrib.auth.models import User
from users.models import *


@task()
def scheduledTask():
    print("hi")