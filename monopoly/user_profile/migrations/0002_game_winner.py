# Generated by Django 4.2.2 on 2023-06-23 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user_profile.user'),
            preserve_default=False,
        ),
    ]
