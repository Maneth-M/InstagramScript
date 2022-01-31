from urllib.request import urlopen
import json

response = urlopen("https://www.instagram.com/web/search/topsearch/?context=blended&query=instagram")

with open('read2.json', 'w') as f:
    json.dump(json.loads(response.read()), f, indent=4)
