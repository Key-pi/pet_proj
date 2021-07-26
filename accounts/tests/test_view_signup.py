from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from ..views import signup
from ..forms import SignUpForm


