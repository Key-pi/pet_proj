from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/blogger/', views.signup_blogger, name='signup_blogger'),
    path('signup/reader/', views.signup_reader, name='signup_reader'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name="password_reset_email.html",
        subject_template_name='password_reset_subject.txt'
    ),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'),
         name='password_reset_done'

         ),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
         name='password_reset_complete'
         ),
    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html'),
         name='password_change'
         ),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
]

SOCIAL_AUTH_URL_NAMESPACE = "social"
