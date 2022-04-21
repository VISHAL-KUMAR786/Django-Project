from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    # def __str__(self) ->str:
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
        pass

    pass


'''
models that how we create database table in django

once we have create we have to migrate your database

one to many relation -> one user can have many item

CharField it is used for simple value like headline , name (simple values)

TextField it give a textarea or message to type something

auto_now_add that mean take a screenshot that i have create this element (sep 11 2022)



Migration -- there are two thing to migrate our database

python manage.py makemigrations ( vase > migrations > 0001_intial.py)
python manage.py migrate

if we change something in our models then we have to run migration command again

'''
