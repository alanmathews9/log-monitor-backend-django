# Generated by Django 4.1.4 on 2023-03-23 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=45, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('hashed_password', models.TextField()),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
