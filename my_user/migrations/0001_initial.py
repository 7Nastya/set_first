# Generated by Django 4.0.5 on 2022-07-21 17:26

from django.db import migrations, models
import my_user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_admin', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='Ник')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('date_joined', models.DateTimeField(blank=True, null=True, verbose_name='Дата присоединения')),
                ('email', models.EmailField(max_length=128, verbose_name='Адрес элктронной почты')),
                ('first_name', models.CharField(max_length=256, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=256, verbose_name='Фамилия')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователя',
            },
            managers=[
                ('objects', my_user.models.UserManager()),
            ],
        ),
    ]