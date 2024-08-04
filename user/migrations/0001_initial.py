# Generated by Django 5.0.7 on 2024-08-04 15:33

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
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
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('current_status', models.CharField(choices=[('Salesman', 'Salesman'), ('Branch Supervisor', 'Branch Supervisor'), ('Department Manager', 'Department Manager'), ('Client', 'Client'), ('Representative', 'Representative')], max_length=40)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BranchGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_members', models.PositiveSmallIntegerField(default=5)),
                ('group', models.ManyToManyField(to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepartmentBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ManyToManyField(to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BranchSupervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.branchgroup')),
                ('departments', models.ManyToManyField(to='user.departmentboard')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('group', models.ManyToManyField(to='auth.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepartmentManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.departmentboard')),
                ('managers_group', models.ManyToManyField(to='user.managergroup')),
            ],
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companies', models.ManyToManyField(to='user.company')),
            ],
        ),
        migrations.CreateModel(
            name='Salesman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_enrolled_branches', models.PositiveSmallIntegerField(default=1)),
                ('branches', models.ManyToManyField(to='user.branchgroup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_state', models.DateField(auto_now=True)),
                ('status', models.IntegerField(choices=[(0, 'Interested'), (1, 'First Meeting'), (2, 'Further Motivation'), (100, 'Acquired'), (-1, 'Lost')], default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.client')),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.salesman')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='employees',
            field=models.ManyToManyField(through='user.Deal', to='user.salesman'),
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(auto_now=True)),
                ('quit_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=40)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
