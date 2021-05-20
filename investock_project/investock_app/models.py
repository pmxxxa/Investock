from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Company(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    company_symbol = models.CharField(max_length=255, blank=True, default='', unique=True)


class YahooStock(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    regular_price = models.DecimalField(decimal_places=2, max_digits=10)
    change = models.DecimalField(max_digits=6, decimal_places=2)
    change_percentages = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(-100.0),
                                                                                         MaxValueValidator(100.0)])
    download_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yahoo_stock = models.ForeignKey(YahooStock, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    creation_time = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edition_time = models.DateTimeField(null=True)


class UserForecast(models.Model):
    forecast_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forecast_price = models.DecimalField(decimal_places=2, max_digits=10)
    excess_or_shortage = models.CharField(max_length=255, null=True)
    difference = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    real_price = models.DecimalField(decimal_places=2, max_digits=10, null=True)

