# Generated by Django 2.1.5 on 2019-02-07 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20190207_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(default=None),
        ),
    ]
