from . import views
from django.urls import path

urlpatterns = [
    path('', views.analizeAccounts, name="analyze-accounts"),
    path('media/', views.analyzeMedia, name="analyze-media"),
    path('account/', views.account, name="analyze-account")
]
