# Generated by Django 3.1.7 on 2023-02-14 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasundayag', '0019_auto_20230214_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnelfunctionipcr',
            name='period',
            field=models.CharField(choices=[('Jan-Jun', 'January to June'), ('Jul-Dec', 'July to December'), ('Select', 'Please select year')], default='Select', max_length=8),
        ),
        migrations.AlterField(
            model_name='personnelsubfunctionipcr',
            name='period',
            field=models.CharField(choices=[('Jan-Jun', 'January to June'), ('Jul-Dec', 'July to December'), ('Select', 'Please select year')], default='Select', max_length=8),
        ),
    ]
