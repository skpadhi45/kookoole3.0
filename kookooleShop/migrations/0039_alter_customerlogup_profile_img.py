# Generated by Django 4.1.3 on 2023-09-14 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kookooleShop', '0038_alter_customerlogup_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerlogup',
            name='profile_img',
            field=models.URLField(default='media/kookoole.png'),
        ),
    ]
