# Generated by Django 5.1.2 on 2024-12-10 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_cart_company_name_alter_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
