import json
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Features, FeaturesCode
from .serializers import FeaturesSerializer, FeaturesCodeSerializer


class FeaturesCodeViewSet(viewsets.ModelViewSet):
    queryset = FeaturesCode.objects.all()
    serializer_class = FeaturesCodeSerializer


class FeaturesViewSet(viewsets.ModelViewSet):
    queryset = Features.objects.all().order_by('datetime')
    serializer_class = FeaturesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ticker', 'timeframe', 'datetime']

    @action(detail=False, methods=['get'], url_path='get-feature-codes')
    def get_feature_codes(self, request):
        features_codes = FeaturesCode.objects.all().values('code')
        features_codes_array = [i['code'] for i in features_codes]
        print('features_codes_array in get_feature_codes:', features_codes_array)
        return Response(json.dumps(features_codes_array))
