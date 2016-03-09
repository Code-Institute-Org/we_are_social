from django import forms
from .models import Thread, Post


class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ['name']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['comment']
