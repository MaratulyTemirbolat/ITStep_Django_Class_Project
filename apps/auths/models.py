from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(
        self,
        email: str,
        password: str
    ) -> 'CustomUser':
        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.set_password(password)  # Для хеширования
        user.save(using=self._db)
        # Когда мы делаем просто save джанго пытается это сохранить туда
        # то, что написано в base.py в DATABASES (смотри 'default')
        # но в проекте может быть несколько баз данных
        # Отличается от save() тем, что в self.__db мы указываем в какую
        # именно базу данных мы сохраняем это(по умолчанию self._db='default')
        # Пример: using='database2' ('database2' должен быть создан в base.py)
        return user

    def create_superuser(
        self,
        email: str,
        password: str
    ) -> 'CustomUser':
        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта/Логин', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    datetime_joined = models.DateTimeField(
        verbose_name='время регистрации',
        default=timezone.now
    )
    USERNAME_FIELD = 'email'
    # Зарезервинованная переменная, чтобы сделать email логином.
    REQUIRED_FIELDS = []
    # Те филды, которые обязательны при создании

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Кастомные пользователи'
        verbose_name = 'Кастомный пользователь'
        ordering = (
            'datetime_joined',
        )

    def __str__(self) -> str:
        return f'Кастомный пользователь: {self.email}'

    def save(self, *args, **kwargs) -> None:
        if self.email != self.email.lower():
            raise ValidationError(
                'Ваш email "%(email)s" должен быть в нижнем регистре',
                code='lower_case_email_error',
                params={'email': self.email}
            )
        super().save(*args, **kwargs)
