from django.db import models
from quote.models import Ticker, Timeframe


class Features(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    timeframe = models.ForeignKey(Timeframe, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    features = models.TextField()

    def __repr__(self):
        return f'{self.ticker} {self.timeframe} {self.datetime} (O: {self.open} H: {self.high} L: {self.low} C: {self.close})'

    def __str__(self):
        return f'{self.ticker} {self.timeframe} {self.datetime} (O: {self.open} H: {self.high} L: {self.low} C: {self.close})'
