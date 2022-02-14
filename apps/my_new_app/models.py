from datetime import datetime

from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from abstracts.models import DateTimeCustom


class Account(DateTimeCustom):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(
        max_length=150
    )
    description=models.TextField()

    class Meta:
        ordering = (
            'full_name',
        )
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
    
    def __str__(self) -> str:
        return f'Аккаунт: {self.user_id} / {self.full_name}'

class Group(DateTimeCustom):
    GROUP_NAME_MAX_LENGTH = 10
    name = models.CharField(
        max_length=GROUP_NAME_MAX_LENGTH
    )
    
    def __str__(self) -> str:
        return f'Группа: {self.name}'
    
    class Meta:
        ordering = (
            'name',
        )
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class StudentQuerySet(QuerySet):
    ADULT_AGE = 18
    
    def get_adult_students(self) -> QuerySet:
        return self.filter(age__gte=self.ADULT_AGE)

class Student(DateTimeCustom):
    MAX_REGISTER_AGE = 30
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE
    )
    age = models.IntegerField(
        'Возраст студента'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT
    )
    gpa = models.FloatField(
        'Среднее значение GPA'
    )
    objects = StudentQuerySet().as_manager()
    
    def __str__(self) -> str:
        return f'Student: {self.account}, Age: {self.age},\
Group: {self.group}, GPA: {self.gpa}'
    
    def save(self,*args,**kwargs) -> None:
        if(self.age > self.MAX_REGISTER_AGE):
            raise ValidationError('Ваш возраст должен \
быть не более %(max_age)s лет',
                code = 'max_possible_age',
                params={'max_age': self.MAX_REGISTER_AGE}
                                  )
        super().save(*args,**kwargs)
    
    def delete(self) -> None:
        datetime_now: datetime = datetime.now()
        self.datetime_deleted = datetime_now
        
        self.save(
            update_fields=['datetime_deleted']
        )
    
    class Meta:
        ordering = (
            'gpa',
        )
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
    

class Professor(DateTimeCustom):
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
        (TOPIC_JAVA,'Java'),
        (TOPIC_PYTHON,'Python'),
        (TOPIC_GOLANG,'Golang'),
        (TOPIC_TYPESCRIPT,'Typescript'),
        (TOPIC_SWIFT,'Swift'),
        (TOPIC_PHP,'PHP'),
        (TOPIC_MATLAB,'MatLab'),
        (TOPIC_SQL,'SQL'),
        (TOPIC_RUBY,'Ruby'),
        (TOPIC_DELPHI,'Delphi')
    )
        
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=FULL_NAME_MAX_LENGTH
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
        
    def save(self,*args,**kwargs) -> None:
        super().save(*args,**kwargs)
        
    def __str__(self) -> str:
        return f'Teacher: {self.full_name}, teaches: {self.topic}'

    
        