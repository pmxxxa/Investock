from datetime import datetime, timedelta, date
from math import fabs

import pytz
from django.contrib.auth import logout, password_validation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed
from .scripts import yahoo_stock_download, historical_data, trend
from .models import YahooStock, Company, Comment, UserForecast
from .serializers import YahooStockSerializer, CommentSerializer, TrendSerializer, UserForecastSerializer, \
    UserSerializer, CompanySerializer
from rest_framework.response import Response


class RegisterView(APIView):

    def post(request):
        serializer = UserSerializer(data=request.DATA)
        if serializer.is_valid():
            User.objects.create_user(
                serializer.init_data['email'],
                serializer.init_data['username'],
                serializer.init_data['password'],
                serializer.init_data['first_name'],
                serializer.init_data['last_name']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


def logout_view(request):
    logout(request)
    return JsonResponse({'msg': 'You have been logout!'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        if not user.check_password(request.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            password_validation.validate_password(request.data.get("new_password"), user=request.user)
        except password_validation.ValidationError as e:
            return Response({"new_password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(request.data.get("new_password"))
        user.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }

        return Response(response)


class UserDetailView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CompanyView(APIView):
    def get(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        return Response(serializer.data)


class YahooStockViewSet(viewsets.ViewSet):
    def list(self, request, pk=None):
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        company_symbol = company.company_symbol
        last_download = YahooStock.objects.filter(company=company).order_by('download_date').last()
        if last_download is None or (last_download.download_date < datetime.now(pytz.utc) - timedelta(hours=1)):
            new_record = yahoo_stock_download(company_symbol)
            regular_price = new_record['regular_price']
            change = new_record['change']
            change_percentages = new_record['change_percentages']
            download_date = new_record['download_time']
            YahooStock.objects.create(company=company, regular_price=regular_price, change=change,
                                      change_percentages=change_percentages,
                                      download_date=download_date)
        queryset = YahooStock.objects.filter(company=company)
        serializer = YahooStockSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = YahooStock.objects.all()
        yahoo_stock = get_object_or_404(queryset, pk=pk)
        serializer = YahooStockSerializer(yahoo_stock)
        return Response(serializer.data)


class CommnetViewSet(LoginRequiredMixin, viewsets.ViewSet):
    def list(self, request, pk):
        queryset = Comment.objects.filter(yahoo_stock_id=pk)
        serializer = CommentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def add(self, request, format=None, pk=None):
        queryset = YahooStock.objects.all()
        yahoo_stock = get_object_or_404(queryset, pk=pk)
        data = {
            "content": request.data.get('content'),
            "user": request.user.pk,
            "yahoo_stock": yahoo_stock.pk
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def edit(self, request, format=None, pk=None):
        comment = Comment.objects.get(id=pk)
        if comment.user.pk != request.user.pk:
            raise MethodNotAllowed(method=request.method)
        comment.edited=True
        comment.edition_time = datetime.now(pytz.utc)
        comment.save()
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comments = Comment.objects.all()
        comment = get_object_or_404(comments, id=pk, user=self.request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrendView(APIView):
    def get(self, request, pk=None):
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        company_symbol = company.company_symbol
        value = trend(historical_data(company_symbol)['adjclose price'])
        serializer = TrendSerializer(value)
        return Response(serializer.data)


class UserForecastViewSet(LoginRequiredMixin, viewsets.ViewSet):
    def list(self, request):
        queryset = UserForecast.objects.filter(user=self.request.user)
        serializer = UserForecastSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create_forecast(self, request):
        data = {
            "user": self.request.user.pk,
            "forecast_date": request.data.get("forecast_date"),
            "forecast_price": request.data.get("forecast_price"),
            "company": request.data.get("company"),
        }
        serializer = UserForecastSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_forecast(self, request, pk=None):
        queryset = UserForecast.objects.all()
        user_forecast = get_object_or_404(queryset, pk=pk, user=self.request.user)
        company_symbol = user_forecast.company.company_symbol
        forecast_date = user_forecast.forecast_date
        if (forecast_date <= date.today() - timedelta(days=1)):
            real_price = historical_data(company_symbol)['adjclose price'][0]
            forecast_price = float(user_forecast.forecast_price)
            difference = fabs(real_price - forecast_price)
            if real_price - forecast_price < 0:
                excess_or_shortage = 'EXCESS'
            else:
                excess_or_shortage = 'SHORTAGE'
            user_forecast.real_price = real_price
            user_forecast.difference = difference
            user_forecast.excess_or_shortage = excess_or_shortage
            user_forecast.save()
            serializer = UserForecastSerializer(user_forecast)
            return Response(serializer.data)
        else:
            serializer = UserForecastSerializer(user_forecast)
            return Response(serializer.data)
