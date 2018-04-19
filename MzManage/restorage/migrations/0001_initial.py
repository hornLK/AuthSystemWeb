# Generated by Django 2.0.2 on 2018-03-31 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32, unique=True)),
                ('moment', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('default', models.BooleanField(db_index=True, default=False)),
                ('permissions', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': '用户角色',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=32, unique=True)),
                ('uesername', models.CharField(max_length=32, unique=True)),
                ('authed', models.BooleanField(default=False)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restorage.Department')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restorage.Role')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(db_index=True, max_length=32, unique=True)),
                ('code', models.CharField(db_index=True, max_length=32, unique=True)),
            ],
            options={
                'verbose_name_plural': '用户类型',
            },
        ),
    ]
