# Generated by Django 5.1.2 on 2024-12-09 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_companyprofile_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
