# Generated by Django 3.0.4 on 2020-04-14 20:59

from django.db import migrations, models
import django.db.models.deletion

from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_delete_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('g_id', models.IntegerField(primary_key=True, serialize=False)),
                ('g_name', models.CharField(max_length=30)),
                ('g_bio', models.TextField()),
            ],
            options={
                'db_table': 'groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GroupData',
            fields=[
                ('g', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='blog.Groups')),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'group_data',
                'managed': False,
            },
        ),
    ]
