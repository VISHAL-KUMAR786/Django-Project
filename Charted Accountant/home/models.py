from django.db import models
from django import forms

# Create your models here.

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=300)
    phone = models.CharField(max_length=13)
    desc = models.TextField(max_length=5000)
    timeStamp = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return f"{self.desc} - {self.email}( {self.name} )"
    pass 

class DateInput(forms.DateInput):
    input_type = 'date'

class CA(models.Model):
    sno = models.AutoField(primary_key=True)
    panNo = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    completed = models.BooleanField()
    # timeStamp = models.DateField(widget=DateInput)
    timeStamp = models.CharField(max_length=10)
    unit = models.CharField(max_length=50)
    email = models.CharField(max_length=300)
    Password = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name 
        
    pass 