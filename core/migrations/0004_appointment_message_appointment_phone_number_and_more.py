# Generated by Django 5.1.4 on 2025-01-07 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Canceled', 'Canceled')], default='Pending', max_length=20),
        ),
    ]