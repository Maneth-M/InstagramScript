from django.shortcuts import render
from django.http.response import HttpResponse
from projects.models import projectAccounts, Project
from instagrapi import Client
import requests

#
cl = Client()
cl.login('lasticeberg', '123AgunamD')


def analizeAccounts(request):
    id = request.GET.get('id')
    project = Project.objects.filter(id=id).first()
    accounts = projectAccounts.objects.filter(project=project).all()

    for account in accounts:
        media = cl.user_medias(account.account.userId, 10)
        print(media)

    return render(request, "analyze/analyze.html", {
        "accounts": accounts,
        "project": project,
        "title": f"{project} - Analyze"
    })