# Generated by Django 4.1 on 2022-10-06 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0003_set_subscription_types"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="valid_until",
            field=models.DateField(db_index=True, verbose_name="Действительно до"),
        ),
    ]
