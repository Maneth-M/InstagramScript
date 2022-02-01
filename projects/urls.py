from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="projects"),
    path('new/', views.new, name="new-project"),
]
