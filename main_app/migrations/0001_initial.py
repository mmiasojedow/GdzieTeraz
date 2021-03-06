# Generated by Django 3.0.2 on 2020-01-30 13:14

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
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa')),
                ('kitchen', models.IntegerField(choices=[(0, ''), (1, 'Amerykańska'), (2, 'Azjatycka'), (3, 'Europejska'), (4, 'Indyjska'), (5, 'Pizza'), (6, 'Polska'), (7, 'Śródziemnomorska'), (8, 'Wegetariańska')], verbose_name='Kuchania')),
                ('address', models.CharField(max_length=128, verbose_name='Adres')),
                ('phone', models.IntegerField(verbose_name='Telefon')),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Nazwa')),
                ('size', models.IntegerField(choices=[(2, 'S'), (4, 'M'), (6, 'L'), (8, 'XL')], verbose_name='Wielkość')),
                ('taken', models.BooleanField(default=False, verbose_name='Zajęty')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Restaurant')),
            ],
        ),
    ]
