# Generated by Django 5.0 on 2024-02-05 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0002_car_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='car/media/uploads/'),
        ),
    ]
