# Generated by Django 5.1.3 on 2024-11-29 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Training", "0004_employeeprofile_required_trainings"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trainingsrequired",
            name="Category",
            field=models.CharField(max_length=20),
        ),
    ]