from instagrapi import Client
import requests


cl = Client()
cl.login('lasticebergs', '123AgunamD')

results = cl.user_info_by_username('instagram').dict()

print(results)

# from ritetag import RiteTagApi
#
# access_token = 'faf974206ee83580738f10f28f670e6a2a6fddf73c40'
# client = RiteTagApi(access_token)
#
# x = client.hashtag_suggestion_for_image("http://127.0.0.1:8000/hashtags/")

