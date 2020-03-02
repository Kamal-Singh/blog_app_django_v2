from django import forms
from django.contrib.auth.models import User
from .models import Blog
class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class CreateBlogForm(forms.ModelForm):
    class Meta():
        model = Blog
        exclude = ('date_created','last_modified','author')