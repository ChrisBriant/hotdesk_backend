# Generated by Django 3.1.3 on 2021-07-07 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210707_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hash',
            field=models.CharField(default='0x4a3b116c852c9af76845d4dada102025', max_length=128),
        ),
    ]