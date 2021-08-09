from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.template.loader import render_to_string
from django.http import JsonResponse

import requests

from .forms import BloggerRegisterForm, ReaderRegisterForm, SignUpForm, ContactForm
from .tasks import send_email_task, contact_form_task


def signup(request):
    return render(request, 'choose_role.html')


def signup_blogger(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        form_user = SignUpForm(request.POST)
        form_blogger = BloggerRegisterForm(request.POST)

        if form_user.is_valid() and form_blogger.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                user = form_user.save()
                blogger = form_blogger.save(commit=False)
                blogger.user = user
                blogger.save()
                form_blogger.save()
                messages.add_message(request, messages.SUCCESS, 'Congratulations, you have successfully registered.')

                if user is not None:
                    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    send_email_task.delay(user.email)
                    return redirect('boards:home')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'signup_blogger.html', context={'form': form_user, 'form1': form_blogger})

        else:
            messages.add_message(request, messages.ERROR, 'Error validations, repeat again')
            return render(request, 'signup_blogger.html', context={'form': form_user, 'form1': form_blogger})

    else:
        form_user = SignUpForm()
        form_blogger = BloggerRegisterForm()

        return render(request, 'signup_blogger.html', context={'form': form_user, 'form1': form_blogger})


def signup_reader(request,  backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":

        form_user = SignUpForm(request.POST)
        form_reader = ReaderRegisterForm(request.POST)

        if form_user.is_valid() and form_reader.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                user = form_user.save()
                reader = form_reader.save(commit=False)
                reader.user = user
                reader.save()
                form_reader.save()
                messages.add_message(request, messages.SUCCESS, "Congratulations, you have successfully registered.")

                if user is not None:
                    auth.login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
                    send_email_task.delay(user.email)
                    return redirect('boards:home')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'signup_reader.html', context={'form': form_user, 'form1': form_reader})
        else:
            return render(request, 'signup_reader.html', context={'form': form_user, 'form1': form_reader})
    else:
        form_user = SignUpForm()
        form_reader = ReaderRegisterForm()
        return render(request, 'signup_reader.html', context={'form': form_user, 'form1': form_reader})


class Login(LoginView):
    model = User
    template_name = 'login.html'

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(self.request, user)
                return redirect('boards:home')
            else:
                messages.error(self.request, 'Incorrect username or password. Please try again.')
                return render(self.request, 'login.html', {'form': form})
        else:
            messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')
            return render(self.request, 'login.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'my_account.html'
    success_message = 'Account successfully updated!)'
    success_url = reverse_lazy('accounts:my_account')

    def get_object(self, queryset=None):
        return self.request.user



def save_board_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            data['form_is_valid'] = True
            data['html_partial_contact'] = render_to_string('contact.html')
        else:
            data['form_is_valid'] = False
    context = {'form': form,
               }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = form.data['name']
        email = form.data['email']
        contact_form_task(email=email, name=name)
    else:
        form = ContactForm()
    return save_board_form(request, form, 'contact.html')









# def contact(request):
#     data = dict()
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#
#             data['form_is_valid'] = True
#             data['html_contact_list'] = render_to_string('base.html', {
#                 'form': form
#             })
#         else:
#             data['form_is_valid'] = False
#     else:
#         form = ContactForm()
#         context = {'form': form}
#         data['html_form'] = render_to_string('contact_form.html', context, request=request)
#         return JsonResponse(data)
