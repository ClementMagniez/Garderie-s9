# Generated by Django 3.1.3 on 2020-11-20 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garderie', '0002_auto_20201116_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='mail',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='name',
        ),
        migrations.RemoveField(
            model_name='parent',
            name='surname',
        ),
    ]