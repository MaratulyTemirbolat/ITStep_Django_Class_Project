from datetime import datetime
from tabnanny import verbose

from django.db import models
from django.db.models import QuerySet
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from abstracts.models import DateTimeCustom
from auths.models import CustomUser


class Group(DateTimeCustom):
    """Group model class."""

    GROUP_NAME_MAX_LENGTH = 10  # max length of the group name
    name = models.CharField(  # field (column in db) representing group name
        max_length=GROUP_NAME_MAX_LENGTH  # max possible length of class name
    )

    def __str__(self) -> str:
        """Magic method that returns name of the instance in print part."""
        return f'Группа: {self.name}'

    class Meta:  # noqa
        ordering = (  # tuple indicates by which fields it needs to sort
            'name',  # sort by field "name" in asc
        )
        verbose_name = 'Группа'  # class name where it is put in single form
        verbose_name_plural = 'Группы'  # class name where it is in plural form


class StudentQuerySet(QuerySet):
    """Exte."""

    ADULT_AGE = 18  # the minimum age of any adult

    def get_adult_students(self) -> QuerySet:  # noqa
        return self.filter(age__gte=self.ADULT_AGE)


class Student(DateTimeCustom):  # noqa
    MAX_REGISTER_AGE = 30
    FULL_NAME_MAX_LENGTH = 150
    account = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name='Пользователь'
    )
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=FULL_NAME_MAX_LENGTH
    )
    age = models.IntegerField(
        verbose_name='Возраст студента'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        verbose_name='Группа'
    )
    gpa = models.FloatField(
        verbose_name='Среднее значение GPA'
    )
    objects = StudentQuerySet().as_manager()

    class Meta:  # noqa
        ordering = (
            'gpa',
        )
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self) -> str:  # noqa
        return 'Student: {0}, Age: {1},Group: {2}, GPA: {3}'.format(
            self.full_name,
            self.age,
            self.group,
            self.gpa
        )

    def save(self, *args, **kwargs) -> None:  # noqa
        if(self.age > self.MAX_REGISTER_AGE):
            raise ValidationError(
                'Ваш возраст должен быть не более %(max_age)s лет',
                code='max_possible_age',
                params={'max_age': self.MAX_REGISTER_AGE}
                                  )
        super().save(*args, **kwargs)

    def delete(self) -> None:  # noqa
        datetime_now: datetime = datetime.now()
        self.datetime_deleted = datetime_now

        self.save(
            update_fields=['datetime_deleted']
        )


class Professor(DateTimeCustom):  # noqa
    FULL_NAME_MAX_LENGTH = 40
    TOPIC_MAX_LENGTH = 30

    TOPIC_JAVA = 'java'
    TOPIC_PYTHON = 'python'
    TOPIC_GOLANG = 'golang'
    TOPIC_TYPESCRIPT = 'typescript'
    TOPIC_SWIFT = 'swift'
    TOPIC_PHP = 'php'
    TOPIC_MATLAB = 'matlab'
    TOPIC_SQL = 'sql'
    TOPIC_RUBY = 'ruby'
    TOPIC_DELPHI = 'delphi'
    TOPIC_CHOICES = (
        (TOPIC_JAVA, 'Java'),
        (TOPIC_PYTHON, 'Python'),
        (TOPIC_GOLANG, 'Golang'),
        (TOPIC_TYPESCRIPT, 'Typescript'),
        (TOPIC_SWIFT, 'Swift'),
        (TOPIC_PHP, 'PHP'),
        (TOPIC_MATLAB, 'MatLab'),
        (TOPIC_SQL, 'SQL'),
        (TOPIC_RUBY, 'Ruby'),
        (TOPIC_DELPHI, 'Delphi')
    )

    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=FULL_NAME_MAX_LENGTH
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.PROTECT
    )
    topic = models.CharField(
        verbose_name='Предмет',
        choices=TOPIC_CHOICES,
        default=TOPIC_JAVA,
        max_length=TOPIC_MAX_LENGTH
    )
    students = models.ManyToManyField('Student')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ('full_name',)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Teacher: {self.full_name}, teaches: {self.topic}'


class StudentHomeworkQuerySet(QuerySet):  # noqa

    def get_non_deleted(self) -> QuerySet:  # noqa
        return self.filter(datetime_deleted__isnull=True)


class StudentHomework(DateTimeCustom):  # noqa
    HOMEWORK_MAX_LENGTH = 100
    title = models.CharField(
        max_length=HOMEWORK_MAX_LENGTH,
        verbose_name='Название'
    )
    subject = models.CharField(
        max_length=HOMEWORK_MAX_LENGTH,
        verbose_name='Предмет'
    )
    logo = models.ImageField(
        upload_to='homeworks/logos/%Y/%m/%d',
        verbose_name='Лого'
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name='Получатель'
    )
    is_checked = models.BooleanField(
        default=False,
        verbose_name='Проверена работа'
    )
    is_passed = models.BooleanField(
        default=True,
        verbose_name='Сдана работа'
    )
    objects = StudentHomeworkQuerySet().as_manager()

    class Meta:  # noqa
        verbose_name = 'Домашка студентов'
        verbose_name_plural = 'Домашки студентов'
        ordering = ('title',)

    def __str__(self) -> str:  # noqa
        return f'Домашка: {self.title}, выполнено: {self.user}'

    def delete(self) -> None:  # noqa
        self.datetime_deleted = datetime.now()
        self.save(
            update_fields=['datetime_deleted']
        )


class FileQuerySet(QuerySet):  # noqa

    def get_checked_homeworks(self) -> QuerySet:  # noqa
        return self.filter(homework__is_checked=True)


class File(DateTimeCustom):  # noqa
    FILE_MAX_LENGHT_NAME = 100
    title = models.CharField(
        max_length=FILE_MAX_LENGHT_NAME,
        verbose_name='Имя файла'
    )
    file = models.FileField(
        upload_to='homeworks/files/%Y/%m/%d',
        verbose_name='Файл'
    )
    homework = models.ForeignKey(
        StudentHomework,
        on_delete=models.PROTECT,
        verbose_name='Домашка'
    )

    class Meta:  # noqa
        verbose_name_plural = 'Файлы'
        verbose_name = 'Файл'
        ordering = ('title',)

    def __str__(self) -> str:  # noqa
        return f'Файл: {self.title} по предмету: {self.homework}'

    def delete(self) -> None:  # noqa
        self.datetime_deleted = datetime.now()
        self.save(
            update_fields=['datetime_deleted']
        )
