# Generated by Django 2.2.9 on 2021-08-30 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210830_1200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',)},
        ),
    ]
