# Generated by Django 3.2.14 on 2022-07-18 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CityWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, unique=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('weather_data', models.JSONField()),
            ],
        ),
    ]