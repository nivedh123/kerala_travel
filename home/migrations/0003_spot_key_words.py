# Generated by Django 4.0.4 on 2022-11-12 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_profilemodel_link_alter_spot_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='key_words',
            field=models.TextField(default=1, help_text='keyword must start with %,keyword just give your contribution more expo!'),
            preserve_default=False,
        ),
    ]