from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Allergy(models.Model):
    name = models.CharField(
        'Название аллергии',
        max_length=50
    )

    class Meta:
        verbose_name = 'Аллергия'
        verbose_name_plural = 'Аллергии'

    def __str__(self):
        return self.name

class SubscriptionType(models.Model):
    name = models.CharField(
        'Название подписки',
        max_length=50
    )
    duration = models.IntegerField(
        'Длительность в днях'
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Тип подписки'
        verbose_name_plural = 'Типы подписки'

    def __str__(self):
        return f'{self.name}, {self.duration} дней, {self.price}р.'

class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Чья подписка',
        related_name='subscriptions',
        on_delete=models.CASCADE,
        db_index=True
    )
    number_of_meals = models.SmallIntegerField(
        'Количество приёмов пищи в день',
    )
    subs_type = models.ForeignKey(
        SubscriptionType,
        verbose_name='Тип подписки',
        related_name='subscriptions',
        on_delete=models.PROTECT,
        db_index=True
    )
    allergies = models.ManyToManyField(
        Allergy,
        verbose_name='Аллергии',
        related_name="subscriptions",
        null=True,
        blank=True
    )
    valid_until = models.DateField(
        'Действительно до',
        db_index=True
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} до {self.valid_until}'
