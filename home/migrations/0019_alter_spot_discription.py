# Generated by Django 4.0.4 on 2022-11-10 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_spot_discription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='discription',
            field=models.TextField(),
        ),
    ]
