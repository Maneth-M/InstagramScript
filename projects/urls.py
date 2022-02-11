from . import views
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('', views.home, name="projects"),
    path('new/', views.new, name="new-project"),
    path('id/', views.displayAccounts, name="display-accounts"),
    path('analyze/', include('analyze.urls'))
]
