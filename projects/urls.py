from . import views
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('', views.projects, name="projects"),
    path('analyze/', include('analyze.urls'))
]
