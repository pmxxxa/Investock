from django.contrib.auth.models import User

from .models import YahooStock, Comment, UserForecast, Company
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class YahooStockSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = YahooStock
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TrendSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=255)


class UserForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserForecast
        fields = '__all__'
