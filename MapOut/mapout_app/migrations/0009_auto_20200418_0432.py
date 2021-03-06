# Generated by Django 3.0.4 on 2020-04-17 20:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mapout_app', '0008_auto_20200418_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='last_modify',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Event Date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tasks',
            name='belong_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapout_app.Project'),
        ),
    ]
