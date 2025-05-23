# Generated by Django 5.1.7 on 2025-04-06 20:48

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_utilisateur_date_naissance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='organisateur',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='date_naissance',
            field=models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2025, 4, 6))]),
        ),
    ]
