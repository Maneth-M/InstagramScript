from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import NewProject
from django.contrib import messages
from .models import Project, projectAccounts


# Home Page
def home(request):
    if request.user.is_authenticated:
        id = request.GET.get('id', '')
        if not id  == "":
            project = Project.objects.filter(id=id).first()
            return render(request, "projects/project.html", {'project': project})
        userId = request.user.username
        user = User.objects.filter(username=userId).first()
        accs = projectAccounts.objects.filter(projects=id).all()
        return render(request, "projects/index.html", {'project_id': user.project_set.all(), "accounts": accs})
    else:
        return redirect('login')


# Create New Project
def new(request):
    if request.method == "POST":
        form = NewProject(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("projects")
        else:
            messages.error(request, "Something went wrong. Please Try again")
    return render(request, "projects/new.html", {"form": NewProject})


def displayAccounts(request):
    print(request.build_absolute_uri())