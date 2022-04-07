# Generated by Django 3.0 on 2022-04-01 13:00

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
            name='StudentHomework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('subject', models.CharField(max_length=100, verbose_name='Предмет')),
                ('logo', models.ImageField(upload_to='homeworks/logos/%Y/%m/%d', verbose_name='Лого')),
                ('is_passed', models.BooleanField(default=True, verbose_name='Сдана работа')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Домашка студентов',
                'verbose_name_plural': 'Домашки студентов',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Время удаления')),
                ('full_name', models.CharField(max_length=150, verbose_name='Полное имя')),
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
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
                'ordering': ('full_name',),
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=100, verbose_name='Имя файла')),
                ('file', models.FileField(upload_to='homeworks/files/%Y/%m/%d', verbose_name='Файл')),
                ('is_checked', models.BooleanField(default=False, verbose_name='Проверена работа')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='my_new_app.StudentHomework', verbose_name='Домашка')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
                'ordering': ('title',),
            },
        ),
    ]
