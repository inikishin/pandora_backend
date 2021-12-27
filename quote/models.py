import uuid
from django.db import models


class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=1000, blank=True, null=True)

    def __repr__(self):
        return f'{self.code} (id: {self.pk})'

    def __str__(self):
        return self.code


class Calendar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=1000, blank=True, null=True)

    def __repr__(self):
        return f'{self.code} (id: {self.pk})'

    def __str__(self):
        return self.code


class Holiday(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=1000)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    holiday_date = models.DateField()

    models.UniqueConstraint(fields=['calendar', 'holiday_date'], name='unique_holidays_in_calendar')

    def __repr__(self):
        return f'{self.holiday_date} - {self.fullname} (id: {self.pk})'

    def __str__(self):
        return f'{self.holiday_date} - {self.fullname}'


class Timeframe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)

    def __repr__(self):
        return f'{self.code} (id: {self.pk})'

    def __str__(self):
        return f'{self.code}'


class MarketType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __repr__(self):
        return f'{self.code} (id: {self.pk})'

    def __str__(self):
        return self.code


class StockExchange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __repr__(self):
        return f'{self.code} (id: {self.pk})'

    def __str__(self):
        return self.code


class Market(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, null=True, blank=True)
    type = models.ForeignKey(MarketType, on_delete=models.CASCADE)
    stock_exchange = models.ForeignKey(StockExchange, on_delete=models.CASCADE)

    # TODO add working hours and days
    def __repr__(self):
        return f'{self.code} (id: {self.pk})'

    def __str__(self):
        return self.code


class Ticker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, null=True, blank=True)
    site = models.CharField(max_length=500, null=True, blank=True)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    models.UniqueConstraint(fields=['code', 'market'], name='unique_ticker_code_in_market')

    def __repr__(self):
        return f'{self.code} (id: {self.pk})'

    def __str__(self):
        return self.code


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    timeframe = models.ForeignKey(Timeframe, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()

    models.UniqueConstraint(fields=['ticker', 'timeframe', 'datetime'],
                            name='unique_quote_for_ticker_timeframe_datetime')

    def __repr__(self):
        return f'{self.ticker} {self.timeframe} {self.datetime} (O: {self.open} H: {self.high} L: {self.low} C: {self.close})'

    def __str__(self):
        return f'{self.ticker} {self.timeframe} {self.datetime} (O: {self.open} H: {self.high} L: {self.low} C: {self.close})'


class BondAdditionalInfo(models.Model):
    ticker = models.OneToOneField(Ticker, on_delete=models.CASCADE, primary_key=True)
    short_name = models.CharField(max_length=1000)
    code_isin = models.CharField(max_length=100, unique=True)
    gov_reg_number = models.CharField(max_length=1000, null=True, blank=True)
    issue_size = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    lot_size = models.FloatField()
    lot_value = models.FloatField()
    min_step = models.FloatField()
    list_level = models.CharField(max_length=1000, null=True, blank=True)
    status = models.CharField(max_length=1000, null=True, blank=True)
    coupon_percent = models.FloatField()
    coupon_period = models.FloatField()
    coupon_value = models.FloatField()
    maturity_date = models.DateTimeField(null=True, blank=True)
    next_coupon_date = models.DateTimeField(null=True, blank=True)
    accumulated_coupon_yield = models.FloatField()

    def __repr__(self):
        return f'{self.ticker.code} (ISIN: {self.code_isin})'

    def __str__(self):
        return f'{self.ticker.code} (ISIN: {self.code_isin})'


class ShareAdditionalInfo(models.Model):
    ticker = models.OneToOneField(Ticker, on_delete=models.CASCADE, primary_key=True)
    change_1w = models.FloatField()
    change_1m = models.FloatField()
    change_3m = models.FloatField()
    change_6m = models.FloatField()
    change_1y = models.FloatField()
