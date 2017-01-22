# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-21 04:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college', models.CharField(max_length=200)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('money', models.IntegerField(default=b'0')),
                ('type', models.BooleanField(choices=[(0, b'Audience'), (1, b'Player')], default=b'0')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
