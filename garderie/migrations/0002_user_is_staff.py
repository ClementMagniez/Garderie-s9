# Generated by Django 3.1.3 on 2021-01-31 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garderie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name="Membre de l'équipe"),
        ),
    ]
