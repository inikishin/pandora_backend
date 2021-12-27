"""
Config module
"""

import os

from quote import models as quote_models
from news import models as news_models

SYNC_TREE = {
    'PCM': {
        'url': os.getenv('PCM_API'),
        'objects': {
            'quotes.currency': {
                'model': quote_models.Currency,
                'url_suffix': '/quotes/currency/',
                'foreign_keys': {}
            },
            'quotes.timeframe': {
                'model': quote_models.Timeframe,
                'url_suffix': '/quotes/timeframe/',
                'foreign_keys': {}
            },
            'quotes.market_type': {
                'model': quote_models.MarketType,
                'url_suffix': '/quotes/market-types/',
                'foreign_keys': {}
            },
            'quotes.stock_exchange': {
                'model': quote_models.StockExchange,
                'url_suffix': '/quotes/stock-exchanges/',
                'foreign_keys': {}
            },
            'quotes.market': {
                'model': quote_models.Market,
                'url_suffix': '/quotes/markets/',
                'foreign_keys': {
                    'type_id': {'linked_object': 'quotes.markettype', 'target_column_name': 'type'},
                    'stock_exchange_id': {'linked_object': 'quotes.stockexchange',
                                          'target_column_name': 'stock_exchange'},
                }
            },
            'quotes.ticker': {
                'model': quote_models.Ticker,
                'url_suffix': '/quotes/tickers/',
                'foreign_keys': {
                    'market_id': {'linked_object': 'quotes.market', 'target_column_name': 'market'},
                }
            },
            'quotes.quote': {
                'model': quote_models.Quote,
                'url_suffix': '/quotes/quotes/',
                'foreign_keys': {
                    'ticker_id': {'linked_object': 'quotes.ticker', 'target_column_name': 'ticker'},
                    'timeframe_id': {'linked_object': 'quotes.timeframe', 'target_column_name': 'timeframe'},
                }
            },
            'quotes.bond_additional_info': {
                'model': quote_models.BondAdditionalInfo,
                'url_suffix': '/quotes/bonds-additional-info/',
                'foreign_keys': {
                    'ticker_id': {'linked_object': 'quotes.ticker', 'target_column_name': 'ticker'},
                    'currency_id': {'linked_object': 'quotes.currency', 'target_column_name': 'currency'},
                }
            },
            'quotes.share_additional_info': {
                'model': quote_models.ShareAdditionalInfo,
                'url_suffix': '/quotes/shares-additional-info/',
                'foreign_keys': {
                    'ticker_id': {'linked_object': 'quotes.ticker', 'target_column_name': 'ticker'},
                }
            },
            'news.tag': {
                'model': news_models.Tag,
                'url_suffix': '/news/tags/',
                'foreign_keys': {}
            },
            'news.source': {
                'model': news_models.Source,
                'url_suffix': '/news/sources/',
                'foreign_keys': {}
            },
            'news.news': {
                'model': news_models.News,
                'url_suffix': '/news/news/',
                'foreign_keys': {
                    'source_id': {'linked_object': 'news.source', 'target_column_name': 'source'},
                    'tags_id': {'linked_object': 'news.tag', 'target_column_name': 'tags'},
                }
            },
        },
    },
    'PTS': {
        'url': os.getenv('PTS_API'),
        'objects': {},
    },
}
