# Generated by Django 4.2.2 on 2023-06-14 21:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0003_alter_group_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
