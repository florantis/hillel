# Generated by Django 4.2.2 on 2023-06-29 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_commentary'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_open', models.BooleanField(auto_created=True)),
                ('assignee', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=32)),
                ('message', models.CharField(max_length=512)),
                ('time_when_posted', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='commentary',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]