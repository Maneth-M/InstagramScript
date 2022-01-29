from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Project

def home(request):
    if request.user.is_authenticated:
        userId = request.user.username
    user = User.objects.filter(username=userId).first()

    return render(request, "projects/index.html", {'project': user.project_set.all()})
1