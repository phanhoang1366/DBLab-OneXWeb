# Generated by Django 5.1.9 on 2025-05-27 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onexweb', '0006_alter_rating_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='authors',
            field=models.ManyToManyField(related_name='novels', to='onexweb.author'),
        ),
        migrations.AlterField(
            model_name='novel',
            name='genres',
            field=models.ManyToManyField(related_name='novels', to='onexweb.genre'),
        ),
    ]
