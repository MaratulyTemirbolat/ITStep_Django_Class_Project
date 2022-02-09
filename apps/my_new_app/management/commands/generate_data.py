import random
from typing import Any
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import (
    User,
)

from my_new_app.models import (
    Group,
    Account,
    Student,
    Professor,
)


class Command(BaseCommand):
    """Custom command for filling up database.

    Generate Test data only for database. 
    For each App you create another own Command
    """
    help = 'Custom command for filling up database.'

    def init(self, *args: tuple, **kwargs: dict) -> None:
        pass

    def _generate_groups(self) -> None: 
        """Generate Group objs."""

        def generate_name(inc: int) -> str:
            return f'Группа {inc}'

        inc: int
        for inc in range(20):
            name: str = generate_name(inc)
            Group.objects.create(
                name=name
            )

    def _generate_accounts_and_students(self) -> None:
        """Generate Account objs."""
        pass
    
    def _generate_professors(self) -> None:
        """Generate Professor objs."""
        pass

    def handle(self, *args: tuple, **kwargs: dict) -> None: # Автоматически вызывается, когда вызывается generate_data файл
        """Handles data filling."""

        start: datetime = datetime.now() # Получаем время в начале срабатывания кода, чтобы высчитать разницу

        self._generate_groups() # Генерируем данные
        self._generate_accounts_and_students()
        self._generate_professors()

        # Выдаем время генерации данных
        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )