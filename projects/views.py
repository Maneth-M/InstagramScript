import datetime
import json

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import NewProject
from django.contrib import messages
from .models import Project, projectAccounts
from accounts.models import instaAccounts
from instagrapi import Client
import requests

#
# cl = Client()
# cl.login('lasticebergs', '123AgunamD')


# Home Page
def home(request):
    if request.user.is_authenticated:
        id = request.GET.get('id', '')
        key = request.GET.get('key', '').lower()
        check = ""
        result = ''

        if not id == "":
            project = Project.objects.filter(id=id).first()
            if not len(key) == 0:
                check = instaAccounts.objects.filter(username=key).first()
                if check is not None:
                    check = instaAccounts.objects.filter(username=key).first().projectaccounts_set.filter(project=project).first()
                if check == None:
                    try:
                        result = cl.user_info_by_username(key).dict()
                        imgResponse = requests.get(result['profile_pic_url_hd'])
                        with open(f"accounts/static/accounts/profilePictures/{result['pk']}.png", 'wb') as f:
                            f.write(imgResponse.content)
                    except Exception as e:
                        print(e)
                        result = "e"
                else:
                    messages.info(request, "Account Already Added")

            if request.method == "POST" and project.size > 0:
                acc = request.POST.get("acc")
                followers = {"today":result['follower_count']}
                following = {"today":result['following_count']}
                media = {"today":result['media_count']}

                check = instaAccounts.objects.filter(username=key).first()

                if check == None:
                    instaAccounts(
                        username=acc.lower(),
                        userId=result['pk'],
                        isVerified=bool(result['is_verified']),
                        isBusiness=result['is_business'],
                        businessCategory=result['business_category_name'],
                        category=result['category_name'],
                        followers=followers,
                        following=following,
                        media=media
                    ).save()

                account = instaAccounts.objects.filter(userId=result['pk']).first()

                projectAccounts(
                    account=account,
                    project=project
                ).save()

                project.size = project.size - 1
                project.save()
                messages.success(request, f"{acc} Added to the Project")
                messages.info(request, f"You have {project.size} Accounts Left")
                check = instaAccounts.objects.filter(username=key).first().projectaccounts_set.filter(project=project).first()

            elif project.size <= 0 :
                messages.error(request, f"You have {project.size} Accounts Left")

            accs = projectAccounts.objects.filter(project=project).all()


            return render(
                request,
                "projects/project.html",
                {
                    'project': project,
                    "results": result,
                    'id': id,
                    'accounts': accs,
                    'check': check
                }
            )

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