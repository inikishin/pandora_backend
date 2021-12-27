from .models import MLModel, FitResults
from rest_framework import serializers


class MLModelSerializer(serializers.ModelSerializer):
    ticker_code = serializers.ReadOnlyField(source='ticker.code')
    timeframe_code = serializers.ReadOnlyField(source='timeframe.code')
    class Meta:
        model = MLModel
        fields = '__all__'
        read_only_fields = ['ticker_code', 'timeframe_code']


class MLModelFitResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitResults
        fields = '__all__'
