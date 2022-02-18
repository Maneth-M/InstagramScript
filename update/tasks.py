from __future__ import absolute_import, unicode_literals
from celery import task
from instagrapi import Client
from accounts.models import instaAccounts
from accounts.models import media as Media
import requests, datetime

cl = Client()
cl.login('lasticebergs', '123AgunamD')

def checkLikes(likes):
    if int(likes) < 0:
        return "hidden"
    else:
        return likes

@task()
def scheduledTask():
    accs = instaAccounts.objects.all()
    if accs is not None:
        for account in accs:
            medias = cl.user_medias(int(account.userId), 10)
            for media in medias:
                if not Media.objects.filter(mediaId=media.pk).exists():
                    if media.video_url:
                        isVideo = True
                        isPhoto = False
                        imgResponse = requests.get(media.video_url)
                        with open(f"accounts/static/accounts/media/videos/{media.pk}.mp4", 'wb') as f:
                            f.write(imgResponse.content)
                    elif media.thumbnail_url:
                        isPhoto = True
                        isVideo = False
                        imgResponse = requests.get(media.thumbnail_url)
                        with open(f"accounts/static/accounts/media/images/{media.pk}.png", 'wb') as f:
                            f.write(imgResponse.content)

                    multiItems = {}
                    if media.resources:
                        isMultiple = True
                        isVideo = False
                        isPhoto = False
                        for it in media.resources:
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

                    hashtags = ""
                    for word in str(media.caption_text).split():
                        if word[0] == "#":
                            hashtags = f"{hashtags}{word} "
                    Media(
                        mediaId=media.pk,
                        user=account,
                        isVideo=isVideo,
                        isPhoto=isPhoto,
                        isMultiple=isMultiple,
                        multiItems=multiItems,
                        likes=checkLikes(media.like_count),
                        comments=media.comment_count,
                        views=media.view_count,
                        Date=media.taken_at,
                        hashtags=hashtags,
                        caption=media.caption_text
                    ).save()

                    account.hashtags = account.hashtags + hashtags
                    account.save()


@task
def getMediaInfo():
    medias = Media.objects.all()
    for media in medias:
        data = cl.media_info(media.mediaId)
        media.dataIn[f"{datetime.datetime.now()}"] = {
            'date': f"{datetime.datetime.now()}",
            'likes': checkLikes(data.like_count),
            'comments': data.comment_count,
            'views': data.view_count
        }
        media.save()

@task
def getUserDate():
    accs = instaAccounts.objects.all()
    for account in accs:
        data = cl.user_info(account.userId)
        account.dataIn[f"{datetime.datetime.now()}"] = {
            'date': f"{datetime.datetime.now()}",
            'followers': data.follower_count,
            'following': data.following_count,
            'posts': data.media_count
        }
        account.save()