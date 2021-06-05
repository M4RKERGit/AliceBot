import re
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


    def getBoardWithTags(self, board, GOT):
        toRet = ""
        allThreads = ""
        toRet += "Рассылка по твоим меткам: "
        for j in range (0, len(GOT)):
            toRet += (GOT[j] + ", ")
        toRet = toRet.rstrip(', ')
        toRet += f'\nДоска /{board}'
        toRet += "\n\n"
        resp = self.apilocal.threads(board)
        for t in resp.threads[:len(resp.threads)]:
            for i in range(0, len(GOT)):
                if re.search(GOT[i].lower(), t.body.lower()):
                    allThreads += f'Сабж: — {t.subject}\nКоличество постов: {t.posts_count} 💬\nПросмотры: {t.views} 👀\nСсылка на ОП-пост: {t.url(board)} ⚡️\nОП-пост: {t.body_text[0:2047]}\n[Конец ОП-поста]'
                    allThreads += '\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
        if len(allThreads) == 0:
            toRet += f'На борде /{board} не найдено тредов по твоим тегам'
            return toRet
        toRet += allThreads
        if len(toRet) > 4000:
            toRet = toRet[0:3980] + '\n[Лимит сообщения]'
        print(toRet)
        return toRet
