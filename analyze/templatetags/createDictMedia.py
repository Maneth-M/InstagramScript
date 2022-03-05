from django.template import Library
import datetime

register = Library()

@register.filter(expects_localtime=True)
def createDictMedia(data):
    new = {}
    dic = dict(data)
    vws = 0
    lks = 0
    cmt = 0
    for key, value in dic.items():
        nvws = int(value['views']) - int(vws)
        nlks = int(value['likes']) - (int(lks))
        ncmt = int(value['comments']) - int(cmt)
        ndate = datetime.datetime.strptime(str(value['date']), "%Y-%m-%d %H:%M:%S.%f")
        new[key] = {
            'date': ndate,
            'views': int(nvws),
            'likes': int(nlks),
            'comments': int(ncmt),
            'cviews': value['views'],
            'clikes': value['likes'],
            'ccomments': value['comments']
        }
        vws = value['views']
        lks = value['likes']
        cmt = value['comments']
    return new.items().__reversed__()