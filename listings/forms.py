from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms

from .models import Listing


class PostAd(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'address', 'state', 'city', 'description', 'price', 'kitchen', 'garage',
                  'garden', 'air_condition', 'extras', 'photo_main', 'photo_1', 'photo_2', 'photo_3')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'address': forms.TextInput(attrs={'placeholder': '1234 Main St'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         'full_name',
    #         Row(
    #             Column('number', css_class='form-group col-md-6 mb-0'),
    #             Column('password', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         'photo',
    #         Row(
    #             Column('password', css_class='form-group col-md-6 mb-0'),
    #             Column('password_2', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Submit('submit', 'Sign Up')
    #     )
