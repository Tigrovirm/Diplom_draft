# Generated by Django 4.2.6 on 2023-12-18 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0008_alter_memory_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memory',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
