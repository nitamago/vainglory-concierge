# Generated by Django 2.0 on 2017-12-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vainpick', '0002_auto_20171204_0246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='pick_heros',
        ),
        migrations.AddField(
            model_name='match',
            name='hero1',
            field=models.CharField(default='no', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='hero2',
            field=models.CharField(default='no', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='hero3',
            field=models.CharField(default='no', max_length=40),
            preserve_default=False,
        ),
    ]
