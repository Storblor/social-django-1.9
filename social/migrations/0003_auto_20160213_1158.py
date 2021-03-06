# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-13 11:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20160212_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('status', models.CharField(max_length=10)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_recip', to='social.Member')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_user', to='social.Member')),
            ],
        ),
        migrations.RemoveField(
            model_name='add',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='add',
            name='to_user',
        ),
        migrations.DeleteModel(
            name='Add',
        ),
    ]
