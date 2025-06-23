from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from userauths.forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.urls import path

from userauths.views import CustomPasswordResetCompleteView

urlpatterns = [
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,
        template_name='userauths/password_reset.html'
    ), name='password_reset'),

    path('forgot-password/sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='userauths/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        form_class=CustomSetPasswordForm,
        template_name='userauths/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset-password/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
