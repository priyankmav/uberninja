"""theuberninja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import StockPortfolioListView, StockPortfolioDetailView, InvestmentDeleteView, InvestmentUpdateView, InvestmentCreateView, StockPortfolioCreateView,StockPortfolioUpdateView, StockPortfolioDeleteView, UserStockPortfolioListView
from . import views

urlpatterns = [
    path('home/', StockPortfolioListView.as_view(), name='stockportfolio-home'),
    path('portfolio/<int:pk>/', StockPortfolioDetailView.as_view(), name='stockportfolio-detail'),
    path('portfolio/investment/<int:pk>/delete/', InvestmentDeleteView.as_view(), name='investment-delete'),
    path('portfolio/investment/<int:pk>/update/', InvestmentUpdateView.as_view(), name='investment-update'),
    path('portfolio/<int:investment_to_portfolio_id>/investment/create/', InvestmentCreateView.as_view(), name='investment-create'),
#    path('accounts/', include("Accounts.urls"),
    path('about/', views.about, name='stockportfolio-about'),
    path('portfolio/new/', StockPortfolioCreateView.as_view(), name='stockportfolio-create'),
    path('portfolio/<int:pk>/update/', StockPortfolioUpdateView.as_view(), name='stockportfolio-update'),
    path('portfolio/<int:pk>/delete/', StockPortfolioDeleteView.as_view(), name='stockportfolio-delete')
]
