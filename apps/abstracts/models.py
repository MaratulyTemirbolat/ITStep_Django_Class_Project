from django.db import models


class DateTimeCustom(models.Model):
    datetime_created = models.DateTimeField(
        verbose_name = "Время создания",
        auto_now_add=True
    )
    datetime_updated = models.DateTimeField(
        verbose_name = "Время обновления",
        auto_now=True
    )
    datetime_deleted = models.DateTimeField(
        verbose_name="Время удаления",
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True
