# Generated by Django 5.1.2 on 2024-12-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_userorder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='date',
            field=models.DateField(null=True),
        ),
    ]