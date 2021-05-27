from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from rest_framework.authtoken import views

from .views import YahooStockViewSet, CommnetViewSet, UserForecastViewSet, logout_view, ChangePasswordView, \
    UserDetailView, CompanyView

yahoo_stock_list = YahooStockViewSet.as_view({'get': 'list'})
yahoo_stock_details = YahooStockViewSet.as_view({'get': 'retrieve'})
comment_list = CommnetViewSet.as_view({'get': 'list'})
comment_details = CommnetViewSet.as_view({'get': 'retrieve'})
add_comment = CommnetViewSet.as_view({'post': 'add'})
edit_comment = CommnetViewSet.as_view({'put': 'edit'})
delete_comment = CommnetViewSet.as_view({'delete': 'delete'})
create_forecast = UserForecastViewSet.as_view({'post': 'create_forecast'})
check_forecast = UserForecastViewSet.as_view({'get': 'check_forecast'})
forecast_list = UserForecastViewSet.as_view({'get': 'list'})

urlpatterns = [
    path('token-auth/', views.obtain_auth_token),
    path('logout/', logout_view),
    path('user-detail/', UserDetailView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('company/', CompanyView.as_view()),
    path('yahoo-stock-list/<int:pk>/', yahoo_stock_list),
    path('yahoo-stock-details/<int:pk>/', yahoo_stock_details),
    path('comment-list/<int:pk>/', comment_list),
    path('comment-details/<int:pk>/', comment_details),
    path('add-comment/<int:pk>/', add_comment),
    path('edit-comment/<int:pk>/', edit_comment),
    path('delete-comment/<int:pk>/', delete_comment),
    path('forecast-list/', forecast_list),
    path('create-forecast/', create_forecast),
    path('check-forecast/<int:pk>/', check_forecast),
    path('accounts/', admin.site.urls),
]
