"""CLI commands for quotes"""
import os
from ftplib import FTP
import pandas as pd

from django.db.models import Max

from quote.models import Quote, Ticker, Timeframe, StockExchange, Currency, \
    Market, BondAdditionalInfo
from api import moex as api_moex


def import_quotes_from_df(df: pd.DataFrame,
                          ticker_code: str,
                          timeframe_code: str) -> int:
    """Loading quotes to database from pandas Dataframe and return imported
    quotes count
    :param df pandas Dataframe with columns 'date_time', 'open', 'high', 'low',
    'close', 'volume'
    :param ticker_code ticker short code
    :param timeframe_code timeframe short code"""

    quotes_imported = 0

    ticker = Ticker.objects.get(code=ticker_code)
    timeframe_d1 = Timeframe.objects.get(code=timeframe_code)

    df['date_time'] = pd.to_datetime(df.date_time)
    df.dropna(inplace=True)

    if len(df) > 0:
        for _, row in df.iterrows():
            Quote.objects.update_or_create(
                ticker=ticker,
                timeframe=timeframe_d1,
                datetime=row['date_time'],
                defaults={'ticker': ticker,
                          'timeframe': timeframe_d1,
                          'datetime': row['date_time'],
                          'open': row['open'],
                          'high': row['high'],
                          'low': row['low'],
                          'close': row['close'],
                          'volume': row['vol']
                          }
            )
            quotes_imported += quotes_imported
        print(f'Loading quotes for {ticker} ended. '
              f'Added {quotes_imported} quotes')

    return quotes_imported


def load_quotes_from_csv_file(ticker_code: str, timeframe_code: str) -> int:
    """Loading quotes from .csv files which stored in catalog defined
    QUOTES_IMPORT_CATALOGS env variable"""
    quotes_imported = 0

    catalogs = os.getenv('QUOTES_IMPORT_CATALOGS').split(';')
    filename = f'{ticker_code.upper()}_{timeframe_code.upper()}.csv'

    files = []
    print(f'Import from catalogs: {catalogs}')
    if len(catalogs) > 0:
        for catalog in catalogs:
            if os.path.isfile(catalog + '/' + filename):
                files.append(catalog + '/' + filename)
    else:
        print('No catalogs in env variable QUOTES_IMPORT_CATALOGS')

    if len(files) == 0:
        print(f'For ticker {ticker_code} no quotes in csv data files')
    elif len(files) > 1:
        print('For ticker {ticker_code} more than one csv file in catalogs. '
              'File list: {files}')
    else:
        history_df = pd.read_csv(files[0])
        quotes_imported = import_quotes_from_df(df=history_df,
                                                ticker_code=ticker_code,
                                                timeframe_code=timeframe_code)

    return quotes_imported


def load_quotes_from_ftp(ticker_code: str, timeframe_code: str) -> int:
    """Loading quotes from ftp"""
    quotes_imported = 0
    print(f'Load quotes from FTP for {ticker_code} {timeframe_code}')

    ftp = FTP(os.getenv('FTP_IP'))
    ftp.login(user=os.getenv('FTP_LOGIN'), passwd=os.getenv('FTP_PASS'))
    ftp.cwd('quotes')
    ftp.retrlines('LIST')

    temp_folder = os.getenv('TEMP_FOLDER')
    if not os.path.isdir(temp_folder):
        os.makedirs(temp_folder)

    filename = f'{ticker_code.upper()}_{timeframe_code.upper()}.csv'
    temp_path = temp_folder + '/' + filename
    with open(temp_path, 'wb') as write_file_path:
        ftp.retrbinary(f'RETR {filename}', write_file_path.write)

    if os.path.isfile(temp_path):
        history_df = pd.read_csv(temp_path)
        os.remove(temp_path)
        quotes_imported = import_quotes_from_df(df=history_df,
                                                ticker_code=ticker_code,
                                                timeframe_code=timeframe_code)

    return quotes_imported


def load_quotes_from_moex_api(ticker_code: str, timeframe_code: str) -> int:
    """Loading quotes from moex api"""
    quotes_imported = 0
    ticker = Ticker.objects.get(code=ticker_code)
    stock_exchange = StockExchange.objects.get(code='moex')
    timeframe_d1 = Timeframe.objects.get(code=timeframe_code)
    max_date = Quote.objects\
        .filter(ticker=ticker, timeframe=timeframe_d1)\
        .aggregate(Max('datetime'))

    if ticker.market.stock_exchange == stock_exchange:
        history_df = api_moex.load_quotes(ticker=ticker.code,
                                          market=ticker.market.type.code,
                                          from_date=max_date['datetime__max'],
                                          interval='24')
        quotes_imported = import_quotes_from_df(df=history_df,
                                                ticker_code=ticker_code,
                                                timeframe_code=timeframe_code)

    return quotes_imported


def load_bonds_list_from_moex() -> int:
    """Loading bonds list from moex api"""
    bonds_imported = 0

    bonds_list = api_moex.get_ticker_list(market='bonds')
    usd_currency = Currency.objects.get(code='USD')
    eur_currency = Currency.objects.get(code='EUR')
    rub_currency = Currency.objects.get(code='RUB')

    for _, bond in bonds_list.iterrows():
        tickers = Ticker.objects.filter(code=bond['code'])
        if len(tickers) == 0:
            moex_market = Market.objects.get(code='moex-bonds')
            ticker = Ticker(code=bond['code'],
                            fullname=bond['fullname'],
                            market=moex_market)
            ticker.save()
        else:
            ticker = tickers[0]

        currency = rub_currency
        if bond['currency'] == 'USD':
            currency = usd_currency
        elif bond['currency'] == 'EUR':
            currency = eur_currency
        elif bond['currency'] != 'SUR':
            raise Exception(f'Unknown currency '
                            f'in bond ticker: {bond["currency"]}')

        BondAdditionalInfo.objects.update_or_create(
            ticker=ticker,
            defaults={
                'ticker': ticker,
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
                'maturity_date': bond['maturity_date']
                    if bond['maturity_date'] != '0000-00-00' else None,
                'next_coupon_date': bond['next_coupon_date']
                    if bond['next_coupon_date'] != '0000-00-00' else None,
                'accumulated_coupon_yield': bond['accumulated_coupon_yield']
            })
        bonds_imported += 1

    print('Loading bonds ended. {bonds_imported} bonds was imported')
    return bonds_imported
