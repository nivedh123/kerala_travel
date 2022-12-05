# Generated by Django 4.0.4 on 2022-11-24 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_spot_options_spot_ref_img_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='ref_img2',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='spot',
            name='ref_img3',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='spot',
            name='ref_img',
            field=models.CharField(help_text='urls/name/', max_length=1000, null=True),
        ),
    ]