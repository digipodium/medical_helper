# Generated by Django 3.2 on 2021-06-15 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_human_resource_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='img',
            field=models.ImageField(default='default_hr.jpg', upload_to='hr/'),
        ),
    ]
