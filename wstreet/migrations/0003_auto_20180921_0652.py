# Generated by Django 2.1.1 on 2018-09-21 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wstreet', '0002_userhistory_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='su',
            name='LiveText',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertable',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]