# Generated by Django 3.1.3 on 2020-11-20 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garderie', '0003_auto_20201120_1902'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parent',
            old_name='uid',
            new_name='user',
        ),
    ]
