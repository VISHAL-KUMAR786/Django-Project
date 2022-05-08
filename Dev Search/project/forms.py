from django import forms
from django.forms import ModelForm
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','featured_image','demo_link','source_code']

    def __init__(self,*args, **kwargs):
        super(ProjectForm,self).__init__(*args, **kwargs)

        for key , field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
                'placeholder': f'Enter your {key}'
            })

        pass 

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels = {
            'value' : 'Place your vote',
            'body' : 'Add a comment with your vote'
        }
        
    def __init__(self,*args, **kwargs):
        super(ReviewForm,self).__init__(*args, **kwargs)

        for key , field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
                'placeholder': f'Enter your {key}'
            })
    pass 