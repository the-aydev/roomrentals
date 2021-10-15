from django import forms
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)
    #is_verified = forms.BooleanField(initial=False)

    class Meta:
        model = User
        fields = ['number', 'email', 'full_name', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['number', 'email', 'full_name', 'photo',
                  'password', 'is_active', 'admin']

    def clean_password(self):
        return self.initial["password"]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)
    #is_verified = forms.BooleanField(initial=False)

    class Meta:
        model = User
        fields = ['full_name', 'number', 'photo', 'email', ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("E-mail is taken")
        return email

    def clean_number(self):
        number = self.cleaned_data.get('number')
        qs = User.objects.filter(number=number)
        if qs.exists():
            raise forms.ValidationError("Number is taken")
        return number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.number = self.cleaned_data['number']
        user.set_password(self.cleaned_data["password"])
        #user.is_verified = False
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    number = PhoneNumberField(widget=forms.TextInput(
        attrs={
            "placeholder": "Phone number",
            "class": "form-control form-control-lg"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Password",
            "class": "form-control form-control-lg"
        }
    ))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        number = data.get("number")
        password = data.get("password")
        user = authenticate(request, number=number, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        self.user = user
        return data
