# Generated by Django 3.1.7 on 2021-06-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]