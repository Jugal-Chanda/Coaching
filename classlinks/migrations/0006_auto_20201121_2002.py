# Generated by Django 3.1.2 on 2020-11-21 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classlinks', '0005_remove_classlink_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classlink',
            name='url',
        ),
        migrations.AddField(
            model_name='subject',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
