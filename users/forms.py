from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import Account


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('email',)


    # class Meta:
    #     model = Account
    #     fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('__all__')


