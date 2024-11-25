# Generated by Django 4.2.16 on 2024-11-05 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reminder',
            options={'verbose_name': 'Напоминание', 'verbose_name_plural': 'Напоминания'},
        ),
        migrations.AddField(
            model_name='reminder',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True, verbose_name='URL'),
        ),
    ]
