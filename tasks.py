import time, datetime
from accounts.models import media

def updateMedia():
    while True:
        m = media.objects.filter(mediaId='2768549031546170731').first()
        m.likeIn = {
            f"{datetime.datetime.now()}": datetime.datetime.now()
        }
        time.sleep(60)

if __name__ == "__main__":
    updateMedia()