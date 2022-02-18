# from instagrapi import Client
# import requests
#
#
# cl = Client()
# cl.login('lasticeberg', '123AgunamD')
#
# medias = cl.user_info(25025320)
#
# print(medias)

from ritetag import RiteTagApi

access_token = 'faf974206ee83580738f10f28f670e6a2a6fddf73c40'
client = RiteTagApi(access_token)

x = client.hashtag_suggestion_for_image("http://127.0.0.1:8000/hashtags/")

