from django.contrib import admin

from .models import Allergy
from .models import Subscription
from .models import SubscriptionType

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(SubscriptionType)
class SubscriptionType(admin.ModelAdmin):
    pass
