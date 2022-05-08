from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name','email','username','password1','password2']
        labels = {
            'first_name' : 'Name'
        }

    def __init__(self,*args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)

        for key , field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
                'placeholder': f'Enter your {key}'
            })

        pass 

class CustomProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','email','username','location','short_intro','bio','profile_image','social_github','social_stackoverflow','social_linkedIn','social_website','social_instagram']

    def __init__(self,*args, **kwargs):
        super(CustomProfileForm,self).__init__(*args, **kwargs)

        for key , field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
                'placeholder': f'Enter your {key}'
            })
    pass 

class skillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name','desc']
        labels = {
            'desc' : 'Description'
        }

    def __init__(self,*args, **kwargs):
        super(skillForm,self).__init__(*args, **kwargs)

        for key , field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
                'placeholder': f'Enter your {key}'
            })
    pass 

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','body']

    def __init__(self,*args, **kwargs):
        super(MessageForm,self).__init__(*args, **kwargs)

        for key , field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
                'placeholder': f'Enter your {key}'
            })