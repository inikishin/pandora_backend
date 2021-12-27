from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.pandora import config, sync

from .models import Market, Timeframe, Ticker, Quote
from .serializers import MarketSerializer, TimeframeSerializer, TickerSerializer, QuoteSerializer


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


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
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
        target = request.data['target']
        target_object = request.data['target_object']

        data = config.SYNC_TREE[target]['objects'][target_object]['model'].objects.all().values()

        sync.sync(target=target, target_object=target_object, data=data)
        return Response({'message': 'synced'})
