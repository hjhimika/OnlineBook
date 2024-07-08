from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Book

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'file_url', 'expiry_date']