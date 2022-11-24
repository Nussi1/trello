from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("username", "email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("username", "email",)


from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)