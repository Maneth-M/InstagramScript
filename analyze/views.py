from django.shortcuts import render
from django.http.response import HttpResponse
from projects.models import projectAccounts, Project
from accounts.models import media as Media
from instagrapi import Client
import requests


cl = Client()
cl.login('lasticeberg', '123AgunamD')


def analizeAccounts(request):
    id = request.GET.get('id')
    project = Project.objects.filter(id=id).first()
    accounts = projectAccounts.objects.filter(project=project).all()

    for account in accounts:
        media = Media.objects.filter(user=account.account).first()
        if media:
            print(media)
        else:
            medias = cl.user_medias(account.account.userId, 10)

            for item in medias:
                if item.media_type == 2:
                    mType = 'video'
                elif item.media_type == 8:
                    mType = 'image'
                else:
                    mType = ""

                if item.video_url:
                    isVideo = True
                    isPhoto = False
                    imgResponse = requests.get(item.video_url)
                    with open(f"accounts/static/accounts/media/videos/{item.pk}.mp4", 'wb') as f:
                        f.write(imgResponse.content)
                elif item.thumbnail_url:
                    isPhoto = True
                    isVideo = False
                    imgResponse = requests.get(item.thumbnail_url)
                    with open(f"accounts/static/accounts/media/images/{item.pk}.png", 'wb') as f:
                        f.write(imgResponse.content)

                multiItems = {}
                if item.resources:
                    isMultiple = True
                    isVideo = False
                    isPhoto = False
                    for it in item.resources:
                        if it.video_url:
                            imgResponse = requests.get(it.video_url)
                            with open(f"accounts/static/accounts/media/videos/{it.pk}.mp4", 'wb') as f:
                                f.write(imgResponse.content)
                            multiItems[f"{it.pk}"] = {
                                "isVideo": True,
                                "id": it.pk
                            }

                        elif it.thumbnail_url:
                            imgResponse = requests.get(it.thumbnail_url)
                            with open(f"accounts/static/accounts/media/images/{it.pk}.png", 'wb') as f:
                                f.write(imgResponse.content)
                            multiItems[f"{it.pk}"] = {
                                "isVideo": False,
                                "id": it.pk
                            }

                else:
                    isMultiple = False
                Media(
                    mediaId=item.pk,
                    user=account.account,
                    isVideo=isVideo,
                    isPhoto=isPhoto,
                    isMultiple=isMultiple,
                    multiItems=multiItems,
                    likes=item.like_count,
                    comments=item.comment_count,
                    views=item.view_count,
                    Date=item.taken_at
                ).save()

    return render(request, "analyze/analyze.html", {
        "accounts": accounts,
        "project": project,
        "title": f"{project} - Analyze"
    })
