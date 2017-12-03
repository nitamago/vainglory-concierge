# Generated by Django 2.0 on 2017-12-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vainpick', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='word_text',
            new_name='pick_heros',
        ),
        migrations.RemoveField(
            model_name='match',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='match',
            name='title',
        ),
        migrations.AddField(
            model_name='match',
            name='match_id',
            field=models.CharField(default='no', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='win',
            field=models.BooleanField(default=False),
        ),
    ]