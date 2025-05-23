# Generated by Django 5.1.2 on 2024-10-09 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livreto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('system', models.CharField(choices=[('marquefacil', 'Marque Facil'), ('observatorio', 'Observatório')], max_length=200, verbose_name='Sistema')),
            ],
        ),
    ]
