from pyexpat import model
from statistics import mode
from django.db import models

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Account(models.Model):
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

class Group(models.Model):
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

class Student(models.Model):
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
    
    def __str__(self) -> str:
        return f'Student: {self.account}, Age: {self.age},\
            Group: {self.group}, GPA: {self.gpa}'
    
    def save(self,*args,**kwargs) -> None:
        if(self.age > self.MAX_REGISTER_AGE):
            raise ValidationError('Ваш возраст должен \
быть не более %(max_age)s лет',
                code = 'max_possible_age',
                params={'max_age':self.MAX_REGISTER_AGE}
                                  )
        super().save(args,kwargs)
            
    
    class Meta:
        ordering = (
            'gpa',
        )
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
    
        