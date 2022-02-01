from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import NewProject
from django.contrib import messages
from .models import Project, projectAccounts
from instagrapi import Client


cl = Client()
cl.login('lasticeberg', '123AgunamD')
# Home Page
def home(request):
    if request.user.is_authenticated:
        id = request.GET.get('id', '')
        acc = request.GET.get('acc', '')
        if not id == "":
            if not acc == "":

            project = Project.objects.filter(id=id).first()
            result = ""
            if request.method == 'POST':
                keyword = request.POST.get('key')
                try:
                    result = cl.user_info_by_username(keyword).dict()
                except:
                    pass
            return render(request, "projects/project.html", {'project': project, "results": result, 'id': id})
        userId = request.user.username
        user = User.objects.filter(username=userId).first()
        return render(request, "projects/index.html", {'project_id': user.project_set.all()})
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