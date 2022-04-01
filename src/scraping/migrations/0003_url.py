# Generated by Django 4.0.3 on 2022-03-31 19:50

from django.db import migrations, models
import django.db.models.deletion
import scraping.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_error'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=scraping.models.default_urls)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Language')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.location', verbose_name='Location')),
            ],
            options={
                'unique_together': {('location', 'language')},
            },
        ),
    ]
