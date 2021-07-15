# Generated by Django 3.1.3 on 2021-07-15 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('desks', '0012_auto_20210715_0457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_booked', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='slot',
            constraint=models.UniqueConstraint(fields=('date',), name='unique_slot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='desk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='desks.desk'),
        ),
        migrations.AddField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.slot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(fields=('slot', 'desk', 'user'), name='unique_booking'),
        ),
    ]