# Generated by Django 3.1.3 on 2021-07-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desks', '0003_auto_20210706_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgemployee',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]