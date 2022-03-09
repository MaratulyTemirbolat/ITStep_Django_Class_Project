# Generated by Django 3.0 on 2022-03-09 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Время удаления')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Время удаления')),
                ('age', models.IntegerField(verbose_name='Возраст студента')),
                ('gpa', models.FloatField(verbose_name='Среднее значение GPA')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_new_app.Group', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
                'ordering': ('gpa',),
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Время удаления')),
                ('full_name', models.CharField(max_length=40, verbose_name='Полное имя')),
                ('topic', models.CharField(choices=[('java', 'Java'), ('python', 'Python'), ('golang', 'Golang'), ('typescript', 'Typescript'), ('swift', 'Swift'), ('php', 'PHP'), ('matlab', 'MatLab'), ('sql', 'SQL'), ('ruby', 'Ruby'), ('delphi', 'Delphi')], default='java', max_length=30, verbose_name='Предмет')),
                ('students', models.ManyToManyField(to='my_new_app.Student')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
                'ordering': ('full_name',),
            },
        ),
    ]
