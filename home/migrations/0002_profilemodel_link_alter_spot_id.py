# Generated by Django 4.0.4 on 2022-11-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='link',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='spot',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
