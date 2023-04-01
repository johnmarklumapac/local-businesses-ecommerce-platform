# Generated by Django 3.1.7 on 2023-03-31 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pasundayag', '0022_auto_20230331_2225'),
        ('account', '0005_auto_20230321_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pasundayag.rank', verbose_name='Rank'),
        ),
    ]
