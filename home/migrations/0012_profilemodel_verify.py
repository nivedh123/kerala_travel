# Generated by Django 4.0.4 on 2022-11-06 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_profilemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='verify',
            field=models.BooleanField(default=False),
        ),
    ]
