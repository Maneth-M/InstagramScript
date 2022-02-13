from django.shortcuts import render
from django.http.response import HttpResponse
from projects.models import projectAccounts, Project
from accounts.models import media as Media
from accounts.models import instaAccounts
from instagrapi import Client
import requests
from django.db.models import Max


cl = Client()
cl.login('lasticeberg', '123AgunamD')


def analizeAccounts(request):
    id = request.GET.get('id')
    project = Project.objects.filter(id=id).first()
    accounts = projectAccounts.objects.filter(project=project).all()
    sort = request.GET.get('sort', "")
    if sort == "":
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
                    checkL = Media.objects.filter(mediaId=item.pk).first()
                    if checkL == None:
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

        accounts = projectAccounts.objects.filter(project=project).all()

        for account in accounts:
            medias = Media.objects.filter(user=account.account).all()
            account.account.views = 0
            account.account.comments = 0
            account.account.likes = 0
            for media in medias:
                account.account.views += int(media.views)
                account.account.likes += int(media.likes)
                account.account.comments += int(media.comments)
            account.account.save()
        # accounts = projectAccounts.objects.filter(project=project).all()
        accounts = projectAccounts.objects.filter(project=project).annotate(Max("account__views")).order_by('-account__views__max')
    elif sort == "V":
        accounts = projectAccounts.objects.filter(project=project).annotate(Max("account__views")).order_by('-account__views__max')
    elif sort == "L":
        accounts = projectAccounts.objects.filter(project=project).annotate(Max("account__likes")).order_by('-account__likes__max')
    elif sort == "C":
        accounts = projectAccounts.objects.filter(project=project).annotate(Max("account__comments")).order_by('-account__comments__max')


    return render(request, "analyze/analyze.html", {
        "accounts": accounts,
        "project": project,
        "title": f"{project} - Analyze",
        "sort": sort
    })


def analyzeMedia(request):
    id = request.GET.get('id')
    sort = request.GET.get("sort", "")
    project = Project.objects.filter(id=id).first()
    accounts = projectAccounts.objects.filter(project=project).all()
    accs = instaAccounts.objects.filter(userId__in=accounts.values('account__userId'))
    print(len(accs))
    if sort == "" or sort == "V":
        media = Media.objects.filter(user__in=accs, isVideo=True).all().annotate(Max("views")).order_by('-views__max')
        charts = {
        }
        for item in media:
            charts[f"{item.pk}"] = [
                ['Date', 'Views']
            ]
            print(item.viewsIn)
            for key, value in dict(item.viewsIn).items():
                charts[f"{item.pk}"].append([key, int(value)])

    elif sort == "L":
        media = Media.objects.filter(user__in=accs).all().annotate(Max("likes")).order_by('-likes__max')
    elif sort == "C":
        media = Media.objects.filter(user__in=accs).all().annotate(Max("comments")).order_by('-comments__max')
    print(len(media))
    return render(request, 'analyze/media.html', {
        "medias": media,
        "sort": sort,
        "project": project,
        "charts": charts
    })
