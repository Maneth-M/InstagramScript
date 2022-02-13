import datetime
from django.db import models
from django.utils.http import int_to_base36
from django.utils import timezone
import uuid, json

def idgen():
    return int_to_base36(uuid.uuid4().int)[:20]

 
# All Accounts Database Model
class instaAccounts(models.Model):
    username = models.CharField(max_length=30)
    userId = models.CharField(primary_key=True, max_length=20, default=idgen)
    followers = models.JSONField(default=dict)
    following = models.JSONField(default=dict)
    medias = models.JSONField(default=dict)
    isVerified = models.BooleanField(default=False)
    isBusiness = models.BooleanField(default=False)
    businessCategory = models.CharField(max_length=50, default=None, blank=True, null=True)
    category = models.CharField(max_length=50, default=None, blank=True, null=True)
    dailyTrending = models.JSONField(default=dict)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.username


# All Media Database Model
class media(models.Model):
    mediaId = models.CharField(primary_key=True, default=idgen, max_length=20)
    user = models.ForeignKey(instaAccounts, on_delete=models.CASCADE)
    isVideo = models.BooleanField(default=False)
    isPhoto = models.BooleanField(default=False)
    isMultiple = models.BooleanField(default=False)
    multiItems = models.JSONField(default=dict)
    likes = models.IntegerField(max_length=20, default="")
    comments = models.IntegerField(max_length=20, default="")
    views = models.IntegerField(max_length=20, default="")
    likeIn = models.JSONField(default=dict)
    commentsIn = models.JSONField(default=dict)
    viewsIn = models.JSONField(default=dict)
    Date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.mediaId
