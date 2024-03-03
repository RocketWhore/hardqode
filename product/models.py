from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    start_date = models.DateTimeField(verbose_name='дата начала')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    is_accessible = models.BooleanField(default=False, verbose_name='доступ')
    min_students = models.PositiveIntegerField(verbose_name='мин. человек')
    max_students = models.PositiveIntegerField(verbose_name='макс. человек')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    students = models.ManyToManyField(User, related_name='product_groups')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    video_link = models.URLField(verbose_name='ссылка на видео')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return self.title


class Accessible(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accessible')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accessible')

    class Meta:
        verbose_name = 'доступ'
        verbose_name_plural = 'доступы'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='ограничение'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.product}'
