# Generated by Django 3.2.9 on 2022-02-22 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='languages',
            field=models.ManyToManyField(blank=True, to='films.Language'),
        ),
    ]
