from . import views
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('', views.home, name="home"),
    path('new/', views.new, name="new-project"),
    path('projects/', views.home, name="my-projects"),
    path('analyze/', include('analyze.urls'))
]
