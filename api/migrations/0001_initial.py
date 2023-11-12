# Generated by Django 4.2.5 on 2023-10-15 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FlightInformation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ride_type", models.CharField(max_length=10)),
                ("flight_time", models.TimeField()),
                ("flight_date", models.DateField()),
                ("dropoff_point", models.CharField(max_length=20)),
                ("airline", models.CharField(max_length=30)),
            ],
        ),
    ]