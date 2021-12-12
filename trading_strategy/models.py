"""
Trading Strategy django app
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from quote.models import Ticker, Timeframe


class TradingStrategy(models.Model):
    """
    Trading strategy model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeframe = models.ForeignKey(Timeframe, on_delete=models.CASCADE, blank=True, null=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, blank=True, null=True)
    filters = models.TextField()
    entrySignals = models.TextField()
    exitSignals = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'{self.fullname} (id: {self.id})'

    def __str__(self):
        return f'{self.fullname}'


class TradingStrategyTestResult(models.Model):
    """
    Trading strategy test result model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trading_strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeframe = models.ForeignKey(Timeframe, on_delete=models.CASCADE, blank=True, null=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, blank=True, null=True)
    filters = models.TextField()
    entrySignals = models.TextField()
    exitSignals = models.TextField()
    test_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return f'{self.trading_strategy} (created_at: {self.created_at})'

    def __str__(self):
        return f'{self.trading_strategy} (created_at: {self.created_at})'


class Signal(models.Model):
    """
    Signal model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trading_strategy = models.ForeignKey(TradingStrategy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    feature_values = models.TextField() # Текущее значение всех фичей для проверки
    signal = models.FloatField()

    def __repr__(self):
        return f'{self.trading_strategy} (signal: {self.signal})'

    def __str__(self):
        return f'{self.trading_strategy} (signal: {self.signal})'
