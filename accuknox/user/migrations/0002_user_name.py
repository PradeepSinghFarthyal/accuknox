# Generated by Django 5.0.3 on 2024-03-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default=None, max_length=254),
        ),
    ]
