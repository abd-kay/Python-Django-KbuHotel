# Generated by Django 3.1.7 on 2021-06-19 01:01

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='detail',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
