# Generated by Django 3.1.7 on 2023-03-18 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pasundayag', '0007_auto_20230318_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipcr',
            old_name='tech_total',
            new_name='core_tech_total',
        ),
    ]
