# Generated by Django 3.1.7 on 2023-02-07 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IPCR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Required', max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, help_text='Not Required', verbose_name='description')),
                ('slug', models.SlugField(max_length=255)),
                ('regular_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999.99.'}}, help_text='Maximum 99999.99', max_digits=7, verbose_name='Regular price')),
                ('discount_price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'The price must be between 0 and 99999.99.'}}, help_text='Maximum 99999.99', max_digits=5, verbose_name='Discount price')),
                ('is_active', models.BooleanField(default=True, help_text='Change ipcr visibility', verbose_name='IPCR visibility')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('stra_e1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('stra_e2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('stra_e3', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('stra_a1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('stra_a2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('stra_a3', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('stra_total', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_q1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_q2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_q3', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_q4', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e3', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e4', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e5', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e6', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e7', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e8', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e9', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e10', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e11', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e12', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e13', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e14', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_e15', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_t1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a3', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a4', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a5', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a6', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a7', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a8', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a9', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a10', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a11', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a12', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a13', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a14', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a15', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a16', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a17', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a18', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_a19', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_total1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('core_total2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_e1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_e2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_e3', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_e4', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_e5', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_t1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_a1', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_a2', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_a3', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_a4', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_a5', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_a6', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('supp_total', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('final_numerical_rating', models.DecimalField(decimal_places=4, default=0.0, max_digits=5)),
                ('final_adjectival_rating', models.CharField(default='Poor', max_length=255, verbose_name='Final Adjectival Rating')),
            ],
            options={
                'verbose_name': 'IPCR',
                'verbose_name_plural': 'IPCRs',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='IPCRSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'IPCR Specification',
                'verbose_name_plural': 'IPCR Specifications',
            },
        ),
        migrations.CreateModel(
            name='IPCRType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required', max_length=255, unique=True, verbose_name='IPCR Name')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Employement Status',
                'verbose_name_plural': 'Employement Status',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required and unique', max_length=255, unique=True, verbose_name='Rank Name')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Rank safe URL')),
                ('is_active', models.BooleanField(default=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pasundayag.rank')),
            ],
            options={
                'verbose_name': 'Rank',
                'verbose_name_plural': 'Ranks',
            },
        ),
        migrations.CreateModel(
            name='IPCRSpecificationValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='IPCR specification value (maximum of 255 words', max_length=255, verbose_name='value')),
                ('ipcr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pasundayag.ipcr')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pasundayag.ipcrspecification')),
            ],
            options={
                'verbose_name': 'IPCR Specification Value',
                'verbose_name_plural': 'IPCR Specification Values',
            },
        ),
        migrations.AddField(
            model_name='ipcrspecification',
            name='ipcr_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pasundayag.ipcrtype'),
        ),
        migrations.CreateModel(
            name='IPCRImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/default.png', help_text='Upload a ipcr image', upload_to='images/', verbose_name='image')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alturnative text', max_length=255, null=True, verbose_name='Alturnative text')),
                ('is_feature', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ipcr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ipcr_image', to='pasundayag.ipcr')),
            ],
            options={
                'verbose_name': 'IPCR Image',
                'verbose_name_plural': 'IPCR Images',
            },
        ),
        migrations.AddField(
            model_name='ipcr',
            name='ipcr_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pasundayag.ipcrtype'),
        ),
        migrations.AddField(
            model_name='ipcr',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pasundayag.rank'),
        ),
        migrations.AddField(
            model_name='ipcr',
            name='users_wishlist',
            field=models.ManyToManyField(blank=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
