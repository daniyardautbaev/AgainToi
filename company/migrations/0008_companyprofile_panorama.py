# Generated by Django 5.1.2 on 2024-12-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='panorama',
            field=models.ImageField(blank=True, help_text='Upload a 360-degree panorama', null=True, upload_to='company/panoramas/'),
        ),
    ]
