# Generated by Django 2.2.3 on 2021-02-15 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210215_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='identification_image',
            field=models.ImageField(upload_to=''),
        ),
    ]
