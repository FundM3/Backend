# Generated by Django 4.1.3 on 2024-05-12 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.apps.project.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('tag_line', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('logo_img', models.ImageField(upload_to=main.apps.project.models.models.project_directory_path)),
                ('x_url', models.URLField(blank=True, null=True)),
                ('github_url', models.URLField(blank=True, null=True)),
                ('telegram_url', models.URLField(blank=True, null=True)),
                ('website_url', models.URLField(blank=True, null=True)),
                ('discord_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=main.apps.project.models.models.project_directory_path)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='project.project')),
            ],
        ),
    ]
