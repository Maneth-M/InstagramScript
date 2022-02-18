from django.shortcuts import render
from ritetag import RiteTagApi

access_token = 'faf974206ee83580738f10f28f670e6a2a6fddf73c40'
client = RiteTagApi(access_token)




def home(request):
    if not request.method == "POST":
        return render(request, "hashtags/hashtags.html")

    txt = request.POST.get('txt')
    img = request.POST.get('img')
    wrd = request.POST.get('wrd')

    if txt:
        result = client.hashtag_suggestion_for_text(wrd)

    if img:
        result = client.hashtag_suggestion_for_image(wrd)

    return render(request, "hashtags/hashtags.html", {
        'data': result
    })