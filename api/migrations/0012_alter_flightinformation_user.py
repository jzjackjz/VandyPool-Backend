# Generated by Django 4.2.5 on 2023-11-23 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0011_alter_timeslot_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flightinformation",
            name="user",
            field=models.CharField(max_length=100),
        ),
    ]