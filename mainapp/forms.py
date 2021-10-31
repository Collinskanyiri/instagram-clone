from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from mainapp.models import *

class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields=('user','username','bio','profile_photo')
        exclude=['user']

class CreateNewPostForm(ModelForm):
    class Meta:
        model=Image
        fields='__all__'
        exclude=['user', 'likes','profile','comments']

