# Generated by Django 2.1.5 on 2021-05-29 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='tags',
            field=models.ManyToManyField(blank=True, to='djangobin.Tag'),
        ),
    ]
