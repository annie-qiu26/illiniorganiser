from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('claimed', models.BooleanField(default=True, help_text='Designates whether a real person has claimed this account.', verbose_name='claimed')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='name')),
                ('abbr', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='abbreviation')),
                ('found_date', models.DateTimeField(verbose_name='date founded')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='date ended')),
                ('summary', models.TextField(default='', max_length=256, verbose_name='summary')),
                ('description', models.TextField(default='', verbose_name='description')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='logo')),
                ('members', models.IntegerField(default=0, verbose_name='number of members')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='organization email')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('last_modified', models.DateTimeField(auto_now_add=True, null=True, verbose_name='last modified')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('category_name', models.CharField(blank=True, max_length=64, verbose_name='category name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'RSOs',
                'verbose_name': 'RSO',
            },
        ),
        migrations.CreateModel(
            name='OrganizationPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('type', models.CharField(choices=[('F', 'FACULTY'), ('A', 'ADMIN'), ('M', 'MODERATOR')], default='M', max_length=1, verbose_name='position type')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='position description')),
                ('holders', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Organization')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'organization positions',
                'verbose_name': 'organization positions',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='tag')),
                ('breadth', models.CharField(choices=[('B', 'BROAD'), ('S', 'SPECIFIC'), ('N', 'NICHE')], default='N', max_length=1, verbose_name='breadth')),
                ('parents', models.ManyToManyField(blank=True, to='app.Tag')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='organization',
            unique_together=set([('name', 'abbr')]),
        ),
    ]
