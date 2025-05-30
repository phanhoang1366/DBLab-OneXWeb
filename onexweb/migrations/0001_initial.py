# Generated by Django 5.1.9 on 2025-05-12 09:11

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=255)),
                ('description', models.TextField(default='The author has not disclosed any information about themselves.')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='author_pictures/')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre_name', models.CharField(max_length=100)),
                ('genre_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('novel_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('cover', models.ImageField(blank=True, null=True, upload_to='novel_covers/')),
                ('status', models.CharField(max_length=50)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('authors', models.ManyToManyField(blank=True, related_name='novels', to='onexweb.author')),
                ('genre', models.ManyToManyField(blank=True, related_name='novels', to='onexweb.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('chapter_id', models.AutoField(primary_key=True, serialize=False)),
                ('chapter_number', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onexweb.novel')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('stars', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onexweb.novel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
