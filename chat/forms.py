from users.models import User
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('photo',)
