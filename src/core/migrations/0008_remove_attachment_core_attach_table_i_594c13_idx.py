# Generated by Django 5.0.6 on 2024-08-08 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_tag_qr_code'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='attachment',
            name='core_attach_table_i_594c13_idx',
        ),
    ]
