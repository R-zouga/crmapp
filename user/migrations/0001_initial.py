# Generated by Django 5.0.7 on 2024-08-25 17:05

import datetime
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=12, unique=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_logout', models.DateTimeField(blank=True, null=True)),
                ('current_status', models.CharField(max_length=40)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('name', models.CharField(max_length=150, primary_key=True, serialize=False, verbose_name='name')),
                ('permissions', models.ManyToManyField(related_name='custom_group_set', to='auth.permission', verbose_name='permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=150)),
                ('phone_number', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user', models.OneToOneField(db_column='user_email', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BranchGroup',
            fields=[
                ('group', models.OneToOneField(db_column='group_name', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.group')),
                ('max_members', models.PositiveSmallIntegerField(default=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepartmentBoard',
            fields=[
                ('group', models.OneToOneField(db_column='group_name', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='user.group'),
        ),
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateField(default=datetime.date.today)),
                ('quit_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Salesman', 'Salesman'), ('Supervisor', 'Supervisor'), ('Manager', 'Manager'), ('Client', 'Client'), ('Representative', 'Representative')], max_length=40)),
                ('belonging_to', models.ForeignKey(db_column='belonging_to_name', on_delete=django.db.models.deletion.CASCADE, related_name='belonging_set', to='user.group')),
                ('responsible_for', models.ForeignKey(db_column='responsible_for_name', null=True, on_delete=django.db.models.deletion.CASCADE, to='user.group')),
                ('user', models.ForeignKey(db_column='user_email', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-join_date'],
            },
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('user', models.OneToOneField(db_column='user_email', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('companies', models.ManyToManyField(to='user.company')),
            ],
        ),
        migrations.CreateModel(
            name='Salesman',
            fields=[
                ('user', models.OneToOneField(db_column='user_email', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('max_enrolled_branches', models.PositiveSmallIntegerField(default=1)),
                ('branches', models.ManyToManyField(to='user.branchgroup')),
            ],
            options={
                'verbose_name_plural': 'Salesmen',
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_state', models.DateField(auto_now_add=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'Interested'), (1, 'First Meeting'), (2, 'Further Motivation'), (100, 'Acquired'), (-1, 'Lost')], default=0)),
                ('service', models.ForeignKey(db_column='service_name', on_delete=django.db.models.deletion.CASCADE, to='service.service')),
                ('service_seeker', models.ForeignKey(db_column='client_email', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('salesman', models.ForeignKey(db_column='salesman_email', on_delete=django.db.models.deletion.CASCADE, to='user.salesman')),
                ('attributed_to', models.ForeignKey(db_column='branch_name', on_delete=django.db.models.deletion.CASCADE, to='user.branchgroup')),
            ],
            options={
                'ordering': ['-date_of_state'],
            },
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('user', models.OneToOneField(db_column='user_email', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('branch_group', models.OneToOneField(db_column='branch_name', on_delete=django.db.models.deletion.CASCADE, to='user.branchgroup')),
                ('departments', models.ManyToManyField(to='user.departmentboard')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerGroup',
            fields=[
                ('group', models.OneToOneField(db_column='group_name', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.group')),
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
                ('department', models.OneToOneField(db_column='department_name', on_delete=django.db.models.deletion.CASCADE, to='user.departmentboard')),
                ('managers_group', models.ManyToManyField(to='user.managergroup')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('first_name', 'last_name')},
        ),
    ]
