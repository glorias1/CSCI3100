# Generated by Django 3.0.4 on 2020-04-22 09:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mapout_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
