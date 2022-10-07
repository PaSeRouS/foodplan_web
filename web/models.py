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
        'Длительность в месяцах'
    )
    price = models.DecimalField(
        'Цена за месяц',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Тип подписки'
        verbose_name_plural = 'Типы подписки'

    def __str__(self):
        return f'{self.name}, {self.duration} мес, {self.price}р. в месяц'


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
    number_of_person = models.SmallIntegerField(
        'Количество персон',
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
        blank=True
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
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


class Ingredient(models.Model):
    name = models.CharField(
        'Название игредиента',
        max_length=50
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredient_quantities',
        on_delete=models.CASCADE
    )
    weight = models.DecimalField(
        'Вес',
        max_digits=7,
        decimal_places=3
    )
    amount = models.DecimalField(
        'Количество',
        max_digits=7,
        decimal_places=3
    )
    unit_title = models.CharField(
        'еденица измерения',
        max_length=20
    )


class Recipe(models.Model):
    name = models.CharField(
        'Название рецепта',
        max_length=50
    )
    steps = models.TextField(
        'Шаги рецепта'
    )
    end_result = models.TextField(
        'Что получилось',
        blank=True
    )
    calories = models.DecimalField(
        'Калории',
        max_digits=4,
        decimal_places=1
    )
    proteins = models.DecimalField(
        'Белки',
        max_digits=4,
        decimal_places=1
    )
    fats = models.DecimalField(
        'Жиры',
        max_digits=4,
        decimal_places=1
    )
    carbs = models.DecimalField(
        'Углеводы',
        max_digits=4,
        decimal_places=1
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through=IngredientQuantity
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
