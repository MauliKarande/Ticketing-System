from django import forms
from .models import User


class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=4)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'department',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AdminUserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'role',
            'department',
            'is_active',
        ]


class AdminPasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=4)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=4)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data
