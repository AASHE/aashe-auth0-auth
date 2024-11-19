# Generated by Django 5.1.2 on 2024-11-19 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Auth0 Organization ID')),
                ('name', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=255)),
                ('metadata', models.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
    ]
