import os
import pandas as pd
from celery import shared_task
from django_pandas.io import read_frame
from django.db.models import Max
from .models import Quote, Market, Timeframe, Ticker, BondAdditionalInfo, Currency, StockExchange
from trading_strategy.models import TradingStrategy, Signal
from core.preprocessing import features, signals
import api.moex as api_moex


@shared_task
def load_quotes_from_moex_api(ticker_code: str) -> None:
    ticker = Ticker.objects.get(code=ticker_code)
    stock_exchange = StockExchange.objects.get(code='moex')
    timeframe_d1 = Timeframe.objects.get(code='d1')
    max_date = Quote.objects.filter(ticker=ticker, timeframe=timeframe_d1).aggregate(Max('datetime'))

    if ticker.market.stock_exchange == stock_exchange:
        history_df = api_moex.load_quotes(ticker=ticker.code, market=ticker.market.type.code, from_date=max_date['datetime__max'], interval='24')
        if len(history_df) > 0:
            for index, row in history_df.iterrows():
                Quote.objects.update_or_create(
                    ticker=ticker, timeframe=timeframe_d1, datetime=row['datetime'],
                    defaults={'ticker': ticker, 'timeframe': timeframe_d1, 'datetime': row['datetime'],
                              'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close'],
                              'volume': row['volume']}
                )
            print(f'Loading quotes for {ticker} ended')


@shared_task
def load_quotes_from_csv_file(ticker_code: str) -> None:
    ticker = Ticker.objects.get(code=ticker_code)
    timeframe_d1 = Timeframe.objects.get(code='D1')
    catalogs = os.getenv('QUOTES_IMPORT_CATALOGS').split(';')
    filename = f'{ticker_code.upper()}_D1.csv'
    files = []
    print(catalogs)
    if len(catalogs) > 0:
        for c in catalogs:
            print(c + '/' + filename)
            if os.path.isfile(c + '/' + filename):
                files.append(c + '/' + filename)
    else:
        print(f'No catalogues in env variable QUOTES_IMPORT_CATALOGS')

    if len(files) == 0:
        print(f'For ticker {ticker_code} no quotes in csv data files')
    elif len(files) > 1:
        print(f'For ticker {ticker_code} more than one csv file in catalogues. File list: {files}')
    else:
        history_df = pd.read_csv(files[0])
        history_df['date_time'] = pd.to_datetime(history_df.date_time)
        history_df.dropna(inplace=True)

        if len(history_df) > 0:
            for index, row in history_df.iterrows():
                Quote.objects.update_or_create(
                    ticker=ticker, timeframe=timeframe_d1, datetime=row['date_time'],
                    defaults={'ticker': ticker, 'timeframe': timeframe_d1, 'datetime': row['date_time'],
                              'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close'],
                              'volume': row['vol']}
                )
            print(f'Loading quotes for {ticker} ended')


@shared_task
def load_bonds_list_from_moex() -> None:
    bonds_list = api_moex.get_ticker_list(market='bonds')
    usd_currency = Currency.objects.get(code='USD')
    eur_currency = Currency.objects.get(code='EUR')
    rub_currency = Currency.objects.get(code='RUB')

    for index, bond in bonds_list.iterrows():
        try:
            ticker = Ticker.objects.get(code=bond['code'])
        except Ticker.DoesNotExist:
            moex_market = Market.objects.get(code='moex-bonds')
            ticker = Ticker(code=bond['code'], fullname=bond['fullname'], market=moex_market)
            ticker.save()

        currency = rub_currency
        if bond['currency'] == 'USD':
            currency = usd_currency
        elif bond['currency'] == 'EUR':
            currency = eur_currency
        elif bond['currency'] != 'SUR':
            raise Exception(f'Unknown currency in bond ticker: {bond["currency"]}')

        BondAdditionalInfo.objects.update_or_create(ticker=ticker,
                                                    defaults=
                                                    {'ticker': ticker,
                                                     'short_name': bond['short_name'],
                                                     'code_isin': bond['code_isin'],
                                                     'gov_reg_number': bond['gov_reg_number'],
                                                     'issue_size': bond['issue_size'],
                                                     'currency': currency,
                                                     'lot_size': bond['lot_size'],
                                                     'lot_value': bond['lot_value'],
                                                     'min_step': bond['min_step'],
                                                     'list_level': bond['list_level'],
                                                     'status': bond['status'],
                                                     'coupon_percent': bond['coupon_percent'],
                                                     'coupon_period': bond['coupon_period'],
                                                     'coupon_value': bond['coupon_value'],
                                                     'maturity_date': bond['maturity_date'] if bond[
                                                                                                   'maturity_date'] != '0000-00-00' else None,
                                                     'next_coupon_date': bond['next_coupon_date'] if bond[
                                                                                                         'next_coupon_date'] != '0000-00-00' else None,
                                                     'accumulated_coupon_yield': bond['accumulated_coupon_yield']}
                                                    );

    print(f'Loading bonds ended')
