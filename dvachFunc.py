import re
import api2ch


class Dvach_Functions(object):
    
    apilocal = None

    def __init__(self):
        self.apilocal = api2ch.Api2ch()


    def getBoardTop(self, GOT):
        cc = 0
        construtedFromDvach = ""
        buf = ""
        pics = ""
        toRet = list()
        toRet.append(f'⚡️⚡️⚡️ТОП ПОСТОВ С ДОСКИ /{GOT.upper()}⚡️⚡️⚡️\n\n')
        resp = self.apilocal.threads(GOT)
        for t in resp.threads[:3]:
            pics = self.getPic(t.url(GOT))
            buf = f'Сабж: {t.subject[0:t.subject.find(".")]}\nКоличество постов: {t.posts_count} 💬\nПросмотры: {t.views} 👀\nСсылка на ОП-пост: {t.url(GOT)} ⚡️\nОП-пост: {t.body_text[0:2047]}\n[Конец ОП-поста]'
            construtedFromDvach = (pics + buf)
            cc += 1
            toRet.append(construtedFromDvach)
        print(toRet)
        return toRet


    def getBoardWithTags(self, board, GOT):
        toRet = list()
        tags = ""
        allThreads = ""
        allPics = ""

        toRet.append(f'\n⚡️⚡️⚡️Доска /{board}⚡️⚡️⚡️')

        resp = self.apilocal.threads(board)
        for t in resp.threads[:len(resp.threads)]:
            for i in range(0, len(GOT)):
                if re.search(GOT[i].lower(), t.body.lower()):
                    allPics = self.getPic(t.url(board))
                    allThreads = f'Сабж: — {t.subject}\nКоличество постов: {t.posts_count} 💬\nПросмотры: {t.views} 👀\nСсылка на ОП-пост: {t.url(board)} ⚡️\nОП-пост: {t.body_text[0:2047]}\n[Конец ОП-поста]'
                    toRet.append(allPics + allThreads)
        if len(allThreads) == 0:
            toRet.append(f'\nНа борде /{board} не найдено тредов по твоим тегам')
            return toRet
        print(toRet)
        return toRet


    def getPic(self, postUrl):
        valid, board, thread_id = api2ch.parse_url(postUrl)
        if not valid:
            print(404, 'Invalid URL')
            return ""
        try:
            thread = self.apilocal.thread(board, thread_id)
        except:
            return ""
        post = thread.posts[0]
        text = ""
        if post.files:
               text += (post.files[0].url() + "\n")
        if len(text) == 0: return "ОП-пик отсутствует"
        return text