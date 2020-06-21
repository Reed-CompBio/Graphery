# Generated by Django 3.0.7 on 2020-06-20 02:27

import backend.model.UserModel
from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 100 characters or fewer. Letters, digits and -/_ only.', max_length=100, unique=True, validators=[backend.model.UserModel.UserNameValidator()])),
                ('email', models.EmailField(error_messages={'unique': 'A user with that username already exists.'}, max_length=255, unique=True)),
                ('is_verified', models.BooleanField(default=True, help_text='Show whether the account is verified')),
                ('role', models.SmallIntegerField(choices=[(60, 'Administrator'), (40, 'author'), (20, 'translator'), (0, 'visitor')], default=0)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category', models.CharField(default='uncategorized', max_length=30, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=100, unique=True)),
                ('categories', models.ManyToManyField(to='backend.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ZHCN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('abstract', models.TextField()),
                ('content_md', models.TextField()),
                ('content_html', models.TextField()),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('tutorial_anchor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.Tutorial')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TutorialCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('code', models.TextField()),
                ('tutorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Tutorial')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=100, unique=True)),
                ('graph_info', models.TextField()),
                ('initial_cyjs', django.contrib.postgres.fields.jsonb.JSONField()),
                ('layouts', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), size=None)),
                ('styles', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(), size=None)),
                ('tutorial', models.ManyToManyField(to='backend.Tutorial')),
            ],
        ),
        migrations.CreateModel(
            name='ExecResultJson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField()),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.TutorialCode')),
                ('graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Graph')),
            ],
        ),
        migrations.CreateModel(
            name='ENUS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
                ('abstract', models.TextField()),
                ('content_md', models.TextField()),
                ('content_html', models.TextField()),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('tutorial_anchor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.Tutorial')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['category'], name='backend_cat_categor_cfa311_idx'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddIndex(
            model_name='tutorial',
            index=models.Index(fields=['url'], name='backend_tut_url_b279e5_idx'),
        ),
        migrations.AddIndex(
            model_name='graph',
            index=models.Index(fields=['url'], name='backend_gra_url_310160_idx'),
        ),
        migrations.AddConstraint(
            model_name='execresultjson',
            constraint=models.UniqueConstraint(fields=('code', 'graph'), name='code exec result constraint'),
        ),
    ]