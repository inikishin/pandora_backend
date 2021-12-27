from django.contrib import admin
from .models import TradingStrategy, Signal


class TradingStrategyAdmin(admin.ModelAdmin):
    list_display = ['fullname']
    ordering = ['fullname']


admin.site.register(TradingStrategy, TradingStrategyAdmin)
admin.site.register(Signal)
