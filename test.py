from instagrapi import Client
import requests


cl = Client()
cl.login('lasticeberg', '123AgunamD')
medias = cl.user_medias(1400246949, 2)

for i in medias:
    print(i)