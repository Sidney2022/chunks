# Generated by Django 4.0.6 on 2022-07-30 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_csvchunk_publishing_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvchunk',
            old_name='chunk_id',
            new_name='file_id',
        ),
    ]
