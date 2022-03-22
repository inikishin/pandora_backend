import uuid
from django.db import models
from quote.models import Ticker, Timeframe


class FeaturesCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255, unique=True)

class Features(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    timeframe = models.ForeignKey(Timeframe, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    features = models.TextField()

    models.UniqueConstraint(fields=['ticker', 'timeframe', 'datetime'],
                            name='unique_quote_for_ticker_timeframe_datetime')

    @staticmethod
    def get_features_parameters():
        return [
            {
                'name': 'MA',
                'code': 'ma8',
                'params': {
                    'period': 8,
                    'extended': True,
                }
            },
            {
                'name': 'MA',
                'code': 'ma13',
                'params': {
                    'period': 13,
                    'extended': True,
                }
            },
            {
                'name': 'MA',
                'code': 'ma21',
                'params': {
                    'period': 21,
                    'extended': True,
                }
            },
            {
                'name': 'MACD',
                'code': 'macd',
                'params': {
                    'fastperiod': 5,
                    'slowperiod': 35,
                    'signalperiod': 3,
                    'extended': True,
                    'divergence': True,
                }
            },
            {
                'name': 'CCI',
                'code': 'cci',
                'params': {
                    'timeperiod': 12,
                    'extended': True,
                    'divergence': True,
                }
            },
            {
                'name': 'Williams',
                'code': 'williams',
                'params': {
                    'timeperiod': 8,
                    'extended': True,
                    'divergence': True,
                }
            },
            {
                'name': 'Bollindger Bands',
                'code': 'bb',
                'params': {
                    'timeperiod': 5,
                    'extended': True,
                }
            },
            {
                'name': 'DivBar',
                'code': 'divbar',
                'params': {}
            },
            {
                'name': 'Hummer',
                'code': 'hummer',
                'params': {}
            },
            {
                'name': 'Shooting star',
                'code': 'shooting_star',
                'params': {}
            },
            {
                'name': 'Regression Line Angle',
                'code': 'regression_line_angle_8',
                'params': {
                    'timeperiod': 8,
                }
            },
            {
                'name': 'Regression Line Angle',
                'code': 'regression_line_angle_35',
                'params': {
                    'timeperiod': 35,
                }
            },
        ]

    def __repr__(self):
        return f'{self.ticker} {self.timeframe} {self.datetime} (O: {self.open} H: {self.high} L: {self.low} C: {self.close})'

    def __str__(self):
        return f'{self.ticker} {self.timeframe} {self.datetime} (O: {self.open} H: {self.high} L: {self.low} C: {self.close})'
