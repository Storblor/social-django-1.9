# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-12 12:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='following',
            field=models.ManyToManyField(related_name='_member_following_+', to='social.Member'),
        ),
        migrations.AddField(
            model_name='add',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_recip', to='social.Member'),
        ),
        migrations.AddField(
            model_name='add',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='add_user', to='social.Member'),
        ),
    ]