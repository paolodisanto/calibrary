# Generated by Django 5.0.6 on 2024-07-04 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SequencialTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=3)),
                ('latest', models.IntegerField(default=0)),
            ],
        ),
    ]
