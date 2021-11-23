from django import forms
from .models import BlogPost



class PostBlog(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ('title', 'image', 'description', 'status')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'image': forms.ImageField(),
			'description': forms.Textarea(attrs={'class': 'form-control'}),			
		}


class EditBlog(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ('title', 'image', 'description', 'status')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'image': forms.ImageField(),
			'description': forms.Textarea(attrs={'class': 'form-control'}),			
		}
