from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
import uuid 

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='user', null=True, blank=True,default='user_default/mehdi.png')
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_stackoverflow = models.CharField(max_length=200, null=True, blank=True)
    social_linkedIn = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    social_instagram = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return str(self.username)
    
    class Meta:
        ordering = ['created']

    @property
    def profileURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url

    pass

class Skill(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return str(self.name)
    pass 


class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    recipient = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True,related_name="messages")
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False,null=True)

    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.subject

    class Meta:
        ordering = ['is_read','-created']