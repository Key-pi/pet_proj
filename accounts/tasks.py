from django.core.mail import send_mail

from myproject.celery import app

from .forms import ContactForm


@app.task
def send_email_task(email):
    send_mail("Congratulations", "Congratulations on registering on our website Django Boards",
              'kd0996253125@gmail.com', [email], fail_silently=False)
    return None


def contact_form_task(email, name):
    send_mail(f"Hello {name} ", "you wanted us to contact you",
              'kd0996253125@gmail.com', [email], fail_silently=False)
    print('hello')
    return None