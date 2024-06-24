# Generated by Django 4.2.13 on 2024-05-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_order_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("admin", "Admin"), ("user", "User")],
                default="user",
                max_length=20,
            ),
        ),
    ]