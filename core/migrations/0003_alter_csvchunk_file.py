# Generated by Django 4.0.6 on 2022-07-27 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_csvchunk_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvchunk',
            name='file',
            field=models.FileField(upload_to='files/<django.db.models.fields.related.ForeignKey>'),
        ),
    ]
