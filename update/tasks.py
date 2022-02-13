from __future__ import absolute_import, unicode_literals
from celery import task
from instagrapi import Client
from accounts.models import instaAccounts
from accounts.models import media as Media
import requests, datetime

cl = Client()
cl.login('daily__ports', 'Buttercup@1234')

@task()
def scheduledTask():
    accs = instaAccounts.objects.all()
    if accs is not None:
        for account in accs:
            medias = cl.user_medias(account.userId, 10)
            for item in medias:
                check = Media.objects.filter(mediaId=item.pk).first()

                if check == None:
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
                            user=account,
                            isVideo=isVideo,
                            isPhoto=isPhoto,
                            isMultiple=isMultiple,
                            multiItems=multiItems,
                            likes=item.like_count,
                            comments=item.comment_count,
                            views=item.view_count,
                            Date=item.taken_at
                        ).save()

                else:
                    print(item.pk)
                    check.likes = item.like_count
                    check.comments = item.comment_count
                    check.views = item.view_count
                    print(type(check.likeIn))
                    check.likeIn[f'{datetime.datetime.utcnow()}'] = item.like_count
                    check.commentsIn[f'{datetime.datetime.utcnow()}'] = item.comment_count
                    check.viewsIn[f'{datetime.datetime.utcnow()}'] = item.view_count
                    check.save()
