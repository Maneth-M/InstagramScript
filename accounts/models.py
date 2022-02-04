from django.db import models
from django.utils.http import int_to_base36
import uuid, json

def idgen():
    return int_to_base36(uuid.uuid4().int)[:20]

class instaAccounts(models.Model):
    username = models.CharField(max_length=30)
    userId = models.CharField(primary_key=True, max_length=20, default=idgen)
    followers = models.JSONField(default=dict)
    following = models.JSONField(default=dict)
    media = models.JSONField(default=dict)
    isVerified = models.BooleanField(default=False)
    isBusiness = models.BooleanField(default=False)
    businessCategory = models.CharField(max_length=50, default=None, blank=True, null=True)
    category = models.CharField(max_length=50, default=None, blank=True, null=True)
    dailyTrending = models.JSONField(default=dict)


    def __str__(self):
        return self.username


