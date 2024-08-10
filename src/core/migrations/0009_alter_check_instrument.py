# Generated by Django 5.0.6 on 2024-08-08 23:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_attachment_core_attach_table_i_594c13_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='core.instrument'),
        ),
    ]
