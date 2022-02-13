from instagrapi import Client
import requests


cl = Client()
cl.login('lasticeberg', '123AgunamD')

medias = cl.user_medias(25025320, 3)
for media in medias:
    print(media)