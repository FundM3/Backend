# Generated by Django 4.1.3 on 2024-05-16 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0002_alter_contribution_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='amount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=30),
        ),
    ]
