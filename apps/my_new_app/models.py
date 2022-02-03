from statistics import mode
from django.db import models

from django.contrib.auth.models import User

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