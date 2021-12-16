from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class LoginUserForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterUserForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if not pw1 or not pw2:
            raise forms.ValidationError("You must provide a password")
        if pw1!=pw2:
            raise forms.ValidationError("Passwords don't match")
        return pw1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class RegisterUserForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if not pw1 or not pw2:
            raise forms.ValidationError("You must provide a password")
        if pw1!=pw2:
            raise forms.ValidationError("Passwords don't match")
        return pw1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ChangeUserForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]
