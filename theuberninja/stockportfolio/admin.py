from django.contrib import admin
from .models import StockPortfolio,Investment
# Register your models here. 

admin.site.register([StockPortfolio, Investment])