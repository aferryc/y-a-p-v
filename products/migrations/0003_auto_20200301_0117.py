# Generated by Django 3.0.3 on 2020-03-01 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_auto_20200301_0112"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="main_image",
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name="product", name="url", field=models.URLField(max_length=300),
        ),
    ]
