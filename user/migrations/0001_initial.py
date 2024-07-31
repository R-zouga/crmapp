# Generated by Django 5.0.7 on 2024-07-30 17:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BranchGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_members', models.PositiveIntegerField(default=5)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BranchSupervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('branch_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.branchgroup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepartmentManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.departmentboard')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='departmentboard',
            name='department_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.departmentmanager'),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('max_enrolled_branches', models.PositiveSmallIntegerField(default=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_state', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Interested'), (1, 'First Meeting'), (2, 'Further Motivation'), (100, 'Acquired'), (-1, 'Lost')], default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.client')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='employees',
            field=models.ManyToManyField(through='user.Deal', to='user.employee'),
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('companies', models.ManyToManyField(to='user.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('date_left', models.DateField(blank=True, null=True)),
                ('branch_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.branchgroup')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='branches',
            field=models.ManyToManyField(through='user.WorkPeriod', to='user.branchgroup'),
        ),
    ]
