from django.urls import path
from .views import convert_currency

urlpatterns = [
    path('', convert_currency, name='convert_currency'),
]
