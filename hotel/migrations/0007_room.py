# Generated by Django 3.1.7 on 2021-06-27 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('price', models.FloatField(blank=True)),
                ('amount', models.IntegerField(blank=True)),
                ('status', models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
            ],
        ),
    ]
