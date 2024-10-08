# Generated by Django 5.0.7 on 2024-09-19 23:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Supervisor', '0001_initial'),
        ('User', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerGroup',
            fields=[
                ('group', models.OneToOneField(db_column='group_name', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='User.group')),
                ('admin', models.ForeignKey(db_column='admin_email', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user', models.OneToOneField(db_column='user_email', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('department', models.OneToOneField(db_column='department_name', on_delete=django.db.models.deletion.CASCADE, to='Supervisor.departmentboard')),
                ('managers_group', models.ManyToManyField(to='Manager.managergroup')),
            ],
        ),
    ]
