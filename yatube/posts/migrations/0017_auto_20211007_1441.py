# Generated by Django 2.2.16 on 2021-10-07 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
    ]
