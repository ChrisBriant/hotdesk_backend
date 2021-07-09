# Generated by Django 3.1.3 on 2021-07-09 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('desks', '0008_building_floor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='floor',
            name='plan',
        ),
        migrations.AddField(
            model_name='building',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='desks.organisation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='floor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='desks.floor'),
            preserve_default=False,
        ),
    ]
