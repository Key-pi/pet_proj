from celery import shared_task

from celery import shared_task
from django.core.mail import send_mail

from myproject.celery import app
from django.core.mail import EmailMessage


@app.task
def send_email_task(email):
    send_mail("Congratulations", "Congratulations on registering on our website",
              'kd0996253125@gmail.com', [email], fail_silently=False)
    return None
