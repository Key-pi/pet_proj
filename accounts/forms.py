from boards.models import Blogger, Categories, Reader

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class DateInput(forms.DateInput):
    input_type = 'date'


class BloggerRegisterForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Categories.objects.all(), required=False)

    class Meta:
        model = Blogger
        fields = ['birthday', 'country', 'city', 'categories']
        widgets = {
            'birthday': DateInput(),
        }


class ReaderRegisterForm(forms.ModelForm):

    class Meta:
        model = Reader
        fields = ['adult', 'interests']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'email')



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()