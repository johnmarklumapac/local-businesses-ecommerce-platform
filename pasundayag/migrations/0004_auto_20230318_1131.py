# Generated by Django 3.1.7 on 2023-03-18 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pasundayag', '0003_auto_20230216_0032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ipcr',
            name='description',
        ),
        migrations.RemoveField(
            model_name='ipcr',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='ipcr',
            name='title',
        ),
        migrations.AddField(
            model_name='ipcr',
            name='period',
            field=models.CharField(choices=[('Select', 'Please select period...'), ('Jan-Jun', 'January to June'), ('Jul-Dec', 'July to December')], default='Select', max_length=8),
        ),
        migrations.AddField(
            model_name='ipcr',
            name='personnel',
            field=models.ForeignKey(default=1, limit_choices_to=models.Q(models.Q(_negated=True, is_superuser=True), models.Q(_negated=True, is_staff=True)), on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ipcr',
            name='year',
            field=models.PositiveSmallIntegerField(default='1997'),
        ),
    ]
