import random
from re import M
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

    def __generate_name(self,
                        name: str,
                        inc: int) -> str:
        return f'{name} {inc}'

    def _generate_users_accounts_students(self) -> None:
        """Generate user account and student objects"""
        
        USER_ACCOUNT_STUDENT_NUMBER = 100
        DEFAULT_PASSWORD = '12345'
        
        def generate_username(increment: int) -> str:
            return f'User {increment}'
        
        def generate_student_age() -> int:
            random_age: int = random.randint(5,Student.MAX_REGISTER_AGE)
            return random_age
        
        def get_random_group() -> Group:
            random_group: Group = random.choice(Group.objects.all())
            return random_group
        
        def get_random_gpa() -> float:
            GPA_MULTIPLIER = 4.0
            HUNDRETH_POSITION = 2
            random_gpa: float = GPA_MULTIPLIER * random.random()
            random_gpa = round(random_gpa,HUNDRETH_POSITION)
            return random_gpa
            
        increment: int 
        for increment in range(USER_ACCOUNT_STUDENT_NUMBER):
            username: str = generate_username(increment)
            is_staff: bool = True
            
            created_user: User = User.objects.create(
                username = username,
                is_staff= is_staff,
                password = DEFAULT_PASSWORD
            )
            
            account_full_name: str = self.__generate_name(username,increment)
            account_description: str = f'{username}\'s description'
            created_account: Account = Account.objects.create(
                user = created_user,
                full_name = account_full_name,
                description = account_description
            )
            student_age: int = generate_student_age()
            student_group: Group = get_random_group()
            student_gpa: float = get_random_gpa()
            Student.objects.create(
                account = created_account,
                age = student_age,
                group = student_group,
                gpa = student_gpa
            )
            
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
    
    def _generate_professors(self) -> None:
        """Generate Professor objs."""
        PROFESSOR_NUMBER = 10
        MIN_STUDENT_NUMBER = 1
        MAX_STUDENT_NUMBER = 5
        
        def get_random_subject_topic() -> str:
            all_subjects: tuple = Professor.TOPIC_CHOICES
            random_subject: str = random.choice(all_subjects)[0]
            return random_subject
        
        inc: int
        for inc in range(PROFESSOR_NUMBER):
            full_name: str = self.__generate_name('Профессор',inc)
            topic: str = get_random_subject_topic()
            created_professor: Professor =  Professor.objects.create(
                full_name = full_name,
                topic = topic
            )
            
            student_number: int = random.randint(
                MIN_STUDENT_NUMBER,
                MAX_STUDENT_NUMBER
                )
            all_students = Student.objects.all()
            unregistered_students: list = random.choices(all_students,k=student_number)
            
            i:int
            for i in range(student_number):
                unregistered_students[i].professor_set.add(
                    created_professor
                    )
            
    def handle(self, *args: tuple, **kwargs: dict) -> None: # Автоматически вызывается, когда вызывается generate_data файл
        """Handles data filling."""

        start: datetime = datetime.now() # Получаем время в начале срабатывания кода, чтобы высчитать разницу

        self._generate_groups() # Генерируем данные
        self._generate_users_accounts_students()
        self._generate_professors()

        # Выдаем время генерации данных
        print(
            'Generating Data: {} seconds'.format(
                (datetime.now()-start).total_seconds()
            )
        )