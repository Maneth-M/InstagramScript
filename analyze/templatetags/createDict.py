from django.template import Library
import datetime

register = Library()

@register.filter(expects_localtime=True)
def createDict(data):
    new = {}
    dic = dict(data)
    flo = 0
    fli = 0
    pst = 0
    for key, value in dic.items():
        nflo = int(value['followers']) - int(flo)
        nfli = int(value['following']) - (int(fli))
        npst = int(value['posts']) - int(pst)
        ndate = datetime.datetime.strptime(str(value['date']), "%Y-%m-%d %H:%M:%S.%f")
        new[key] = {
            'date': ndate,
            'followers': int(nflo),
            'following': int(nfli),
            'posts': int(npst),
            'cfollowers': value['followers'],
            'cfollowing': value['following'],
            'cposts': value['posts']
        }
        flo = value['followers']
        fli = value['following']
        pst = value['posts']
    return new.items().__reversed__()