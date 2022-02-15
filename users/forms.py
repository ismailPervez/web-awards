from dataclasses import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, ModelForm, Textarea
from django.forms.widgets import Textarea
from .models import Post, Review

class RegisterForm(UserCreationForm):
    email = EmailField(max_length=50)

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class CreateNewPost(ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'link',
            'desc',
            'preview_image'
        ]

        labels = {
            'desc': 'description',
            'preview_image': 'preview image'
        }

class CreateReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['content']

        widgets = {
            'content': Textarea(attrs={'placeholder': 'post your review...'})
        }

        labels = {
            'content': ''
        }