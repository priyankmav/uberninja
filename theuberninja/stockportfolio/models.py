from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.urls import reverse_lazy, reverse

# Create your models here.
class StockPortfolio(models.Model):
    stock_portfolio_name = models.CharField(max_length=20, null=False, default="Portfolio")
    stock_portfolio_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    @property
    def investments(self):
        return Investment.objects.filter(investment_to_portfolio=self)

    def get_absolute_url(self):
            return reverse('stockportfolio-detail', kwargs={'pk': self.pk})
    
    #def get_absolute_url(self):
    #    return reverse('post-detail', kwargs={'pk': self.pk})

class Investment(models.Model):
    investment_to_portfolio = models.ForeignKey(StockPortfolio, on_delete=models.CASCADE)
    investment_name = models.CharField(max_length=50)
    investment_type = models.CharField(max_length=20)
    investment_ticker = models.CharField(max_length=20)
    investment_units = models.DecimalField(max_digits=12, decimal_places=2)
    investment_price = models.DecimalField(max_digits=8, decimal_places=2)
    date_purchased = models.DateTimeField(default=timezone.now)

    @property
    def total_price(self):
        return self.investment_units*self.investment_price
    
    def __str__(self):
        return self.investment_name 