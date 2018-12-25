# Generated by Django 2.0.7 on 2018-09-20 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidPrice', models.IntegerField(default=0)),
                ('bidShares', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('NumberOfshares', models.IntegerField(default=10)),
                ('sharePrice', models.IntegerField(default=0)),
                ('remainingShares', models.IntegerField(default=10)),
                ('PEratio', models.FloatField(default=0.0)),
                ('sixtyFlag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField(default=-1)),
                ('noShares', models.IntegerField(default=0)),
                ('cash', models.IntegerField(default=400000)),
                ('netWorth', models.IntegerField(default=0)),
                ('isSU', models.BooleanField(default=False)),
                ('noOfCompanies', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellPrice', models.IntegerField(default=0)),
                ('sellShares', models.IntegerField(default=0)),
                ('tenflag', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Company')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='SU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spread', models.IntegerField(default=0)),
                ('sensex', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noShares', models.IntegerField(default=0)),
                ('pricesShare', models.IntegerField(default=0)),
                ('buysell', models.IntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Company')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noShares', models.IntegerField(default=0)),
                ('pricesShare', models.IntegerField(default=0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Company')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='buytable',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Company'),
        ),
        migrations.AddField(
            model_name='buytable',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wstreet.Profile'),
        ),
    ]