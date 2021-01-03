# Generated by Django 3.1.3 on 2020-12-19 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garderie', '0008_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('paid', models.BooleanField()),
                ('date_start', models.DateTimeField(verbose_name='Date de départ')),
                ('date_end', models.DateTimeField(verbose_name='Date de fin')),
            ],
        ),
        migrations.CreateModel(
            name='HourlyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('date_start', models.DateTimeField(verbose_name='Date de départ')),
                ('date_end', models.DateTimeField(verbose_name='Date de fin')),
            ],
        ),
        migrations.CreateModel(
            name='ReliablePerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('parents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garderie.parent')),
            ],
        ),
        migrations.DeleteModel(
            name='Config',
        ),
        migrations.RemoveField(
            model_name='child',
            name='name',
        ),
        migrations.RemoveField(
            model_name='child',
            name='surname',
        ),
        migrations.AddField(
            model_name='child',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='child',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='recurring',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garderie.child'),
        ),
        migrations.AddField(
            model_name='bill',
            name='rate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='garderie.hourlyrate'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='rate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='garderie.hourlyrate'),
        ),
    ]
