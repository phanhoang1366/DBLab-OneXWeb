# Generated by Django 5.1.9 on 2025-05-13 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onexweb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='abstract',
        ),
    ]
