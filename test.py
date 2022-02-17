from instagrapi import Client
import requests


cl = Client()
cl.login('lasticeberg', '123AgunamD')

medias = cl.user_info(25025320)

print(medias)