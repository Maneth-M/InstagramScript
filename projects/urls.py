from . import views
from django.urls import path
from analyze.views import analizeAccounts

urlpatterns = [
    path('', views.home, name="projects"),
    path('new/', views.new, name="new-project"),
    path('id/', views.displayAccounts, name="display-accounts"),
    path('analyze/', analizeAccounts, name="analyze-accounts"),
]
