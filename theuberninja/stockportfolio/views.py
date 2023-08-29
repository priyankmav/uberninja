from typing import Any, Optional
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .models import StockPortfolio
from .models import Investment
from .forms import InvestmentForm

# Create your views here.

def home(request):
    context = {
        'portfolios': StockPortfolio.objects.all()
    }
    return render(request, 'stockportfolio/home.html', context)

class StockPortfolioListView(LoginRequiredMixin, ListView):
    model = StockPortfolio
    template_name =  "stockportfolio/home.html" #  <app>/<model>_<viewtype>.html
    context_object_name = 'portfolios'
    login_url = reverse_lazy("login")
    def get_queryset(self):
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        user = self.request.user
        return StockPortfolio.objects.filter(stock_portfolio_user=user)


class StockPortfolioDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView ):
    model = StockPortfolio
    template_name =  "stockportfolio/stockportfolio_detail.html"
    context_object_name = 'stockportfolios'
    login_url = reverse_lazy("login")
    #context_object_name = 'investments'
    # def get_queryset(self):
    #     #user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     #user = self.request.user
    #     #stock_portfolio = self.model.id
    #     return Investment.objects.filter(investment_to_portfolio=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
            context = super(StockPortfolioDetailView, self).get_context_data(**kwargs)
            context['investments'] = Investment.objects.filter(investment_to_portfolio=self.kwargs['pk'])
            return context
    
    def test_func(self):
        stockportfolio = self.get_object()
        if self.request.user == stockportfolio.stock_portfolio_user:
            return True
        return False

class InvestmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Investment
    def get_success_url(self):
        investment_to_portfolio = self.object.investment_to_portfolio
        return reverse_lazy('stockportfolio-detail', kwargs={'pk': investment_to_portfolio.pk }) 
    def test_func(self):
        investment = self.get_object()
        stockportfolio = StockPortfolio.objects.get(pk=investment.investment_to_portfolio.pk)
        if self.request.user == stockportfolio.stock_portfolio_user:
            return True
        return False

class InvestmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Investment
    template_name = "stockportfolio/investment_update_form.html"
    fields = ['investment_name', 'investment_type', 'investment_ticker', 'investment_units', 'investment_price']

    def form_valid(self, form):
        return super().form_valid(form)
    
    def test_func(self):
        investment = self.get_object()
        stockportfolio = StockPortfolio.objects.get(pk=investment.investment_to_portfolio.pk)
        if self.request.user == stockportfolio.stock_portfolio_user:
            return True
        return False

    def get_success_url(self):
        investment_to_portfolio = self.object.investment_to_portfolio
        return reverse_lazy('stockportfolio-detail', kwargs={'pk': investment_to_portfolio.pk }) 

class InvestmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Investment
    form_class = InvestmentForm
    template = 'stockportfolio/investment_form.html'  # Replace with your template name

    def form_valid(self, form):
        portfolio_id = self.kwargs['investment_to_portfolio_id']
        portfolio = StockPortfolio.objects.get(pk=portfolio_id)
        form.instance.investment_to_portfolio = portfolio
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_to_portfolio_id'] = self.kwargs['investment_to_portfolio_id']
        return context
    
    def get_success_url(self):
        investment_to_portfolio = self.object.investment_to_portfolio
        return reverse_lazy('stockportfolio-detail', kwargs={'pk': investment_to_portfolio.pk }) 
    
    def test_func(self):
        investment = self.get_object()
        stockportfolio = StockPortfolio.objects.get(pk=investment.investment_to_portfolio.pk)
        if self.request.user == stockportfolio.stock_portfolio_user:
            return True
        return False

class UserStockPortfolioListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Investment
    template_name =  "stockportfolio/user_stocks.html" #  <app>/<model>_<viewtype>.html
    context_object_name = 'stocks'


class StockPortfolioCreateView(LoginRequiredMixin, CreateView):
    model = StockPortfolio
    fields = ['stock_portfolio_name']
    success_url = "/"
    def form_valid(self, form):
        form.instance.stock_portfolio_user = self.request.user
        return super().form_valid(form)

class StockPortfolioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StockPortfolio
    fields = ['stock_portfolio_name']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class StockPortfolioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = StockPortfolio
    success_url = "/"
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        
def about(request):
    return render(request, 'stockportfolio/about.html', {'title': 'About'})