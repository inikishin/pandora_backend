from django.core.management.base import BaseCommand

from quote.models import Timeframe, Ticker
from quote.helper import load_quotes_from_ftp


class Command(BaseCommand):
    help = """
    Loading quotes from different sources. Specify first argument as data, second is source.
    """

    def add_arguments(self, parser):
        parser.add_argument('data',
                            nargs='?',
                            choices=['quotes', 'bonds'],
                            type=str,
                            help='Please select data type to import from list')
        parser.add_argument('source',
                            nargs='?',
                            choices=['ftp', 'api', 'files'],
                            type=str,
                            help='Please select data source from list')

    def handle(self, *args, **options):
        if options['data'] == 'quotes':
            if options['source'] == 'ftp':
                print('loading quotes from ftp')
                timeframe = Timeframe.objects.get(code='D1')
                tickers = Ticker.objects.all()
                for ticker in tickers:
                    load_quotes_from_ftp(ticker_code=ticker.code, timeframe_code=timeframe.code)
            else:
                print('This source is unavailable for data type {}'.format(options['data']))
        elif options['data'] == 'bonds':
            if options['source'] == 'api':
                print('loading bonds from api')

            else:
                print('This source is unavailable for data type {}'.format(options['data']))
        else:
            print('Unknown data option. Please type "python manage.py import --help" to see available options')
