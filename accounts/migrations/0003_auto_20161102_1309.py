# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-02 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_turma_disciplina'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='codigo',
            field=models.CharField(editable=False, max_length=4, unique=True),
        ),
    ]
