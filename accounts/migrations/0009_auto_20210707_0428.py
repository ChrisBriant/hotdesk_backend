# Generated by Django 3.1.3 on 2021-07-07 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210707_0427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hash',
            field=models.CharField(default='0xf0170f7162c503bf36d3bac49f9a71dd', max_length=128),
        ),
    ]
