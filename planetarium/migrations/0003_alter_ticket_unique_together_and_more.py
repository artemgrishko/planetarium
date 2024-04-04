# Generated by Django 5.0.3 on 2024-04-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("planetarium", "0002_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="astronomyshow",
            name="show_theme",
            field=models.ManyToManyField(
                blank=True, related_name="astronomy_shows", to="planetarium.showtheme"
            ),
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("show_session", "row", "seat"), name="unique_ticket"
            ),
        ),
    ]