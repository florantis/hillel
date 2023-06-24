# Generated by Django 4.2.2 on 2023-06-23 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_trophy_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trophy',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='trophy',
            name='time_when_recieved',
        ),
        migrations.CreateModel(
            name='GrantedTrophy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_when_recieved', models.TimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.user')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.grantedtrophy')),
            ],
        ),
    ]
