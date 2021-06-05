from api2ch import Api2ch


class Dvach_Functions(object):
    
    apilocal = None

    def __init__(self):
        self.apilocal = Api2ch()

    def getBoardTop(self, GOT):
        construtedFromDvach = ""
        resp = self.apilocal.threads(GOT)
        for t in resp.threads[:3]:
            buf = f'Сабж: — {t.subject}\nКоличество постов: {t.posts_count} 💬\nПросмотры: {t.views} 👀\nСсылка на ОП-пост: {t.url(GOT)} ⚡️\nОП-пост: {t.body_text[0:2047]}\n[Конец ОП-поста]'
            construtedFromDvach += (buf + '\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
        toRet = f'ТОП ПОСТОВ С ДОСКИ /{GOT.upper()}\n\n' + construtedFromDvach
        if len(toRet) > 4000:
            toRet = toRet[0:3980] + '\n[Лимит сообщения]'
        print(toRet)
        return toRet