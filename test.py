from instagrapi import Client
import requests

#
# cl = Client()
# cl.login('lasticebergs', '123AgunamD')
#
# results = cl.user_info_by_username('instagram').dict()
#
# print(results)

from ritetag import RiteTagApi

access_token = 'dbe703b234cfae50a3baf8e4fa74aee3cb3d11a94ad2'
client = RiteTagApi(access_token)

x = client.hashtag_suggestion_for_image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/1200px-Image_created_with_a_mobile_phone.png")
for item in x:
    print(item.hashtag)