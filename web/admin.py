from django.contrib import admin

from .models import (Ingredient,
                     IngredientQuantity,
                     Recipe,
                     Allergy,
                     Subscription,
                     SubscriptionType,
                     SubscriptionRecipe)


class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 0


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass


class SubscriptionRecipesInline(admin.TabularInline):
    model = SubscriptionRecipe
    extra = 3


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionRecipesInline]


@admin.register(SubscriptionType)
class SubscriptionType(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        IngredientQuantityInline,
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
