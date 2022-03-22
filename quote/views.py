import json

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_pandas.io import read_frame

from api.pandora import config, sync

from daily_analysis.models import Features, FeaturesCode
from core.preprocessing.features import extend_dataframe_with_features
from .models import Market, Timeframe, Ticker, Quote
from .serializers import MarketSerializer, TimeframeSerializer, TickerSerializer, QuoteSerializer
from .tasks import load_quotes_from_moex_api
from .tasks import load_quotes_from_csv_file


class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class TimeframeViewSet(viewsets.ModelViewSet):
    queryset = Timeframe.objects.all()
    serializer_class = TimeframeSerializer


class TickerViewSet(viewsets.ModelViewSet):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['market']
    search_fields = ['code', 'fullname']

    @action(detail=True, methods=['post'], url_path='load-quotes')
    def load_quotes(self, request, pk=None):
        ticker = Ticker.objects.get(pk=pk)

        if ticker.market.stock_exchange.code == 'moex':
            source = 'api moex'
            load_quotes_from_moex_api.delay(ticker.code)
        else:
            source = 'file'
            load_quotes_from_csv_file.delay(ticker.code)

        print(f'Loading quotes for ticker {ticker} with pk: {pk} from {source}')
        print(f'Request data: {request.data}')

        return Response({'message': 'ok'})


    @action(detail=True, methods=['post'], url_path='processing-features')
    def processing_features(self, request, pk=None):
        ticker = Ticker.objects.get(pk=pk)
        print(f'Processing features for ticker {ticker} with pk: {pk}')
        print(f'Request data: {request.data}')

        timeframe_d1 = Timeframe.objects.get(code='d1')
        quotes = Quote.objects.filter(ticker=ticker, timeframe=timeframe_d1)
        feature_params = Features.get_features_parameters()
        print(f'get features params {feature_params}')
        df_with_features = extend_dataframe_with_features(read_frame(quotes), feature_params)
        print(f'calc new df with features {df_with_features.columns}')
        print(f'calc new df with features {df_with_features.tail()}')

        print(f'update features codes')
        FeaturesCode.objects.all().delete()
        for column_code in df_with_features.columns[8:]:
            FeaturesCode(code=column_code).save()

        df_with_features.dropna(inplace=True)
        if len(df_with_features) > 0:
            for index, row in df_with_features.iterrows():
                Features.objects.update_or_create(
                    ticker=ticker, timeframe=timeframe_d1, datetime=index,
                    defaults={'ticker': ticker, 'timeframe': timeframe_d1, 'datetime': index,
                              'open': row['open'], 'high': row['high'], 'low': row['low'], 'close': row['close'], 'volume': row['volume'],
                              'features': json.dumps([row[i] for i in df_with_features.columns[8:]])}
                )

        print('write to base')
        return Response({'message': 'ok'})


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all().order_by('datetime')
    serializer_class = QuoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ticker', 'timeframe', 'datetime']

    @action(detail=False, methods=['get'], url_path='sync-config')
    def sync_config(self, request):
        response_sync_tree = config.SYNC_TREE.copy()

        for target in response_sync_tree.keys():
            for target_object in response_sync_tree[target]['objects'].keys():
                response_sync_tree[target]['objects'][target_object]['model'] = str(response_sync_tree[target]['objects'][target_object]['model'])

        print(response_sync_tree)
        return Response(response_sync_tree)

    @action(detail=False, methods=['post'])
    def sync(self, request):
        print('sync request data', request.data)
        target = request.data['target']
        target_object = request.data['target_object']

        print('object', config.SYNC_TREE[target]['objects'][target_object]['model'])
        data = config.SYNC_TREE[target]['objects'][target_object]['model'].objects.all().values()

        sync.sync(target=target, target_object=target_object, data=data)
        return Response({'message': 'synced'})
