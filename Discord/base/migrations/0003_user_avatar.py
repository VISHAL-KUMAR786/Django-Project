# Generated by Django 3.2.7 on 2022-05-07 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20220507_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='base-default/avatar.svg', null=True, upload_to='base'),
        ),
    ]
