from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from tinymce import models as tinymce_models

# Create your models here.
# Database    -->     Excel workbook
# Model in Django  --->   table        -->     Sheet


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=20)
    slug = models.CharField(max_length=150)
    timeStamp = models.DateTimeField(blank=True)
    image = models.ImageField(upload_to='Blog/images', default="")
    view = models.IntegerField(default=0)
    # content = models.TextField()
    content = tinymce_models.HTMLField()

    def __str__(self):
        return f"{self.title} by {self.author}"
    pass


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.comment[:40] + '... ' + "by " + self.user.username
    pass
