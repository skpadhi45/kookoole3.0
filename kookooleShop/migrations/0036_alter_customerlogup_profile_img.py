# Generated by Django 4.1.3 on 2023-08-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kookooleShop', '0035_alter_customerlogup_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerlogup',
            name='profile_img',
            field=models.ImageField(blank=True, default='kookoole.png', upload_to='media/'),
        ),
    ]