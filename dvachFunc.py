from api2ch import Api2ch

class Dvach_Functions(object):
    api = Api2ch()

    def getBoard(self, GOT):
        construtedFromDvach = ""
        resp = self.api.threads(GOT)
        for t in resp.threads[:3]:
            buf = f'Сабж: — {t.subject}\nКоличество постов: {t.posts_count} 💬\nПросмотры: {t.views} 👁\nОП-пост: {t.body_text[0:2047]}\n[Конец ОП-поста]'
            construtedFromDvach += (buf + '\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
        toRet = construtedFromDvach
        if len(toRet) > 4000:
            toRet = toRet[0:3980] + '\n[Лимит сообщения]'
        print(toRet)
        return toRet