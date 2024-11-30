# Generated by Django 5.1.3 on 2024-11-29 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Training", "0003_alter_employeeprofile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeeprofile",
            name="required_trainings",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Training.trainingsrequired",
            ),
        ),
    ]