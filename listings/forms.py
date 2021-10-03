from django import forms

from .models import Listing


class PostAd(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'address', 'state', 'city', 'description', 'price', 'kitchen', 'garage',
                  'garden', 'air_condition', 'extras', 'photo_main', 'photo_1', 'photo_2', 'photo_3',)

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'address': forms.TextInput(attrs={'placeholder': '1234 Main St'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description'}),
        }
