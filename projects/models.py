from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.http import int_to_base36
import uuid
from accounts.models import instaAccounts


def idgen():
    return int_to_base36(uuid.uuid4().int)[:20]


class Project(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=idgen)
    name = models.CharField(max_length=50)
    cDate = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.IntegerField(default=25)

    def __str__(self):
        return self.name


class projectAccounts(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=idgen)
    account = models.ForeignKey(instaAccounts, on_delete=models.CASCADE, default=idgen)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    visiblity = models.BooleanField(default=True)

    def __str__(self):
        return str(self.account)


