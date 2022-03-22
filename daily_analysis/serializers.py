from .models import Features, FeaturesCode
from rest_framework import serializers


class FeaturesSerializer(serializers.ModelSerializer):
    ticker_code = serializers.ReadOnlyField(source='ticker.code')
    timeframe_code = serializers.ReadOnlyField(source='timeframe.code')
    class Meta:
        model = Features
        fields = '__all__'
        read_only_fields = ['ticker_code', 'timeframe_code']


class FeaturesCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturesCode
        fields = '__all__'
