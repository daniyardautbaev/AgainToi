# Generated by Django 5.1.2 on 2024-12-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userorder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
