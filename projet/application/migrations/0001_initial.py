# Generated by Django 5.1.7 on 2025-03-23 14:57

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_depart', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=250)),
                ('prenoms', models.CharField(max_length=300)),
                ('numero', models.CharField(max_length=250)),
                ('date_naissance', models.DateField(validators=[django.core.validators.MaxValueValidator(datetime.date(2025, 3, 23))])),
                ('role', models.CharField(choices=[('admin', 'Administrateur'), ('utilisateur', 'Utilisateur')], default='utilisateur', max_length=20)),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.departement')),
            ],
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('statut', models.CharField(choices=[('present', 'Présent'), ('absent', 'Absent'), ('excuse', 'Excusé')], max_length=10)),
                ('notes', models.TextField(blank=True, null=True)),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.evenement')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.utilisateur')),
            ],
        ),
        migrations.AddField(
            model_name='evenement',
            name='organisateur',
            field=models.ForeignKey(limit_choices_to={'role': 'admin'}, on_delete=django.db.models.deletion.CASCADE, to='application.utilisateur'),
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.evenement')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.utilisateur')),
            ],
        ),
    ]
