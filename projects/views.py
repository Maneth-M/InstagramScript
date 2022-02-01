from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import NewProject
from django.contrib import messages
from .models import Project, projectAccounts
from instagrapi import Client
# from accounts.models import accounts

cl = Client()
cl.login('lasticeberg', '123AgunamD')
# Home Page
def home(request):
    if request.user.is_authenticated:
        id = request.GET.get('id', '')
        key = request.GET.get('key', '')
        result = False
        if not id == "":
            if not key == "":
                try:
                    result = cl.user_info_by_username(key).dict()
                except:
                    result = "e"
            project = Project.objects.filter(id=id).first()
            if request.method == "POST":
                acc = request.POST.get("acc")
                print(acc)
                print(project)
                instance = projectAccounts(username=acc, project=project).save()
                messages.success(request, f"{acc} Added to the Project")
            accs = projectAccounts.objects.filter(project=project).all()
            print(len(accs))
            return render(request, "projects/project.html", {'project': project, "results": result, 'id': id, 'accounts': accs})

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