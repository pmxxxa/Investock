from django.contrib import admin
from .models import *


class YahooStockAdmin(admin.ModelAdmin):
    download_date = models.DateTimeField()


admin.site.register(YahooStock, YahooStockAdmin)
admin.site.register(Company)
admin.site.register(Comment)
admin.site.register(UserForecast)
