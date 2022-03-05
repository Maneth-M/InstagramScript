import datetime
import json

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import NewProject
from django.contrib import messages
from .models import Project, projectAccounts
from accounts.models import instaAccounts, media
from instagrapi import Client
import requests
from ritetag import RiteTagApi

access_token = 'dbe703b234cfae50a3baf8e4fa74aee3cb3d11a94ad2'
client = RiteTagApi(access_token)

cl = Client()
cl.login('butterbunny23', 'Buttercup@1234')


# Home Page

def index(request):
    if request.user.is_authenticated:
        userId = request.user.username
        hashtags = ""
        if request.method == "POST":
            txt = request.POST.get('txt')
            tp = request.POST.get('tp')
            if txt:
                if tp == "wrd":
                    hashtags = client.hashtag_suggestion_for_text(txt)

                elif tp == "img":
                    hashtags = client.hashtag_suggestion_for_image(txt)

                user = User.objects.filter(username=userId).first()
                return render(request, "projects/index.html", {
                    "user": user,
                    "projects":  user.project_set.all(),
                    "form": NewProject,
                    "hashtags": hashtags
                })
            form = NewProject(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
                return redirect("index")
            else:
                messages.error(request, "Something went wrong. Please Try again")

        user = User.objects.filter(username=userId).first()
        return render(request, "projects/index.html", {
            "user": user,
            "projects":  user.project_set.all(),
            "form": NewProject,
            "hashtags": hashtags
        })
    else:
        return redirect('login')


def projects(request):
    result = None
    check = True
    if request.user.is_authenticated:

        if request.method == "POST":
            act = request.POST.get("act")
            projectId = request.POST.get("id")
            key = request.POST.get("key")
            project = Project.objects.filter(id=projectId).first()
            if act == "delete":
                project.delete()
                messages.warning(request, "Project Deleted")
                return redirect("index")
            account = instaAccounts.objects.filter(username=key.lower()).first()
            if act == "add":
                if project.size > 0:
                    projectAccounts(
                        account=account,
                        project=project
                    ).save()
                    project.size = project.size - 1
                    project.save()
                    messages.success(request, f"{key} Added to the Projects")
                else:
                    messages.error(request, f"Project is Full")

            elif act == "remove":
                projectAccounts.objects.filter(account=account, project=project).first().delete()
                project.size += 1
                project.save()
                messages.success(request, f"{key} Removed")
            return render(
                request,
                "projects/viewProject.html",
                {
                    "accounts": projectAccounts.objects.filter(project=projectId).all(),
                    "project": Project.objects.filter(id=projectId).first(),
                    "result": result,
                    "check": check,
                }
            )
        projectId = request.GET.get("id", "")
        userId = request.user.username
        key = request.GET.get("key", "")
        if key:
            if not instaAccounts.objects.filter(username=key.lower()).exists():
                try:
                    result = cl.user_info_by_username(key).dict()
                    if result['is_private']:
                        messages.warning(request, "Private Account")
                        return render(
                            request,
                            "projects/viewProject.html",
                            {
                                "accounts": projectAccounts.objects.filter(project=projectId).all(),
                                "project": Project.objects.filter(id=projectId).first(),
                                "result": result,
                                "check": check
                            }
                        )
                    imgResponse = requests.get(result['profile_pic_url_hd'])
                    with open(f"accounts/static/accounts/profilePictures/{result['pk']}.png", 'wb') as f:
                        f.write(imgResponse.content)
                    followers = {"today":result['follower_count']}
                    following = {"today":result['following_count']}
                    posts = {"today":result['media_count']}
                    instaAccounts(
                        username=key.lower(),
                        userId=result['pk'],
                        isVerified=bool(result['is_verified']),
                        isBusiness=result['is_business'],
                        businessCategory=result['business_category_name'],
                        category=result['category_name'],
                        followers=followers,
                        following=following,
                        medias=posts,
                        bio=result['biography']
                    ).save()
                except Exception as e:
                    messages.error(request, "Something went wrong. Please Try again")
            if projectAccounts.objects.filter(project=Project.objects.filter(id=projectId).first(), account=instaAccounts.objects.filter(username=key.lower()).first()).exists():
                messages.warning(request, "Account Already Added")
            return render(
                request,
                "projects/viewProject.html",
                {
                    "accounts": projectAccounts.objects.filter(project=projectId).all(),
                    "project": Project.objects.filter(id=projectId).first(),
                    "result": instaAccounts.objects.filter(username=key.lower()).first(),
                    "check": projectAccounts.objects.filter(project=Project.objects.filter(id=projectId).first(), account=instaAccounts.objects.filter(username=key.lower()).first()).exists()

                }
            )


        user = User.objects.filter(username=userId).first()
        if user.project_set.filter(id=projectId).exists():
            return render(
                request,
                "projects/viewProject.html",
                {
                    "accounts": projectAccounts.objects.filter(project=projectId).all(),
                    "project": Project.objects.filter(id=projectId).first(),
                    "result": result,
                    "check": check
                }
            )
    else:
        return redirect("login")