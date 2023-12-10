from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, \
    UserCreationForm
from django.contrib.auth.password_validation import validate_password

from management.mixins import FormControlMixin

from .models import Role, User


class UserForm(FormControlMixin, UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_password, ])
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all()
    )

    class Meta:
        model = User
        fields = (
            'avatar', 'username', 'email', 'first_name', 'last_name', 'patronymic', 'roles'
        )
        fields_order = fields

    def save(self, commit=True):

        instance = super().save(commit=False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # instance.groups_set.clear()
            # print(self.cleaned_data['groups'])
            for role in self.cleaned_data['roles']:
                instance.roles.add(role)


        self.save_m2m = save_m2m

        instance.save()
        self.save_m2m()

        return instance


class LoginUserForm(FormControlMixin, AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}), required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
                               required=True)