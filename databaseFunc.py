import json
from pydantic import BaseModel
import time
from typing import List


class UserModel(BaseModel):
    userName : str
    chatId : int
    boardsList : List[str]
    tagsList : List[str]

class DatabaseModel(BaseModel):
    #database : str
    totalUsers : int
    curDate : str
    userList : List[UserModel]

class Database():

    class User():
        userName = "DefaultName"
        chatId = 0000
        boardsList = list()
        tagsList = list()
        
        def __init__(self, name, id, bList, tList):
            self.userName = name
            self.chatId = id
            self.boardsList = bList
            self.tagsList = tList

        def addBoard(self, recBoard):
            for i in range(0, len(self.boardsList)):
                if recBoard == self.boardsList[i]:
                    self.boardsList.pop(i)
                    return f'Борда {recBoard} удалена из твоего списка'
            self.boardsList.append(recBoard)
            return f'Борда {recBoard} добавлена в твой список'


        def addTag(self, recTag):
            for i in range(0, len(self.tagsList)):
                if recTag == self.tagsList[i]:
                    self.tagsList.pop(i)
                    return f'Тег {recTag} удален из твоего списка'
            self.tagsList.append(recTag)
            return f'Тег {recTag} добавлен в твой список'


    database = None
    totalUsers = 0
    curDate = "01.01.1970"
    userList = list()

    def __init__(self):
        self.totalUsers = 0
        self.curDate = "01.01.1970"
        self.userList = list()
        self.getDatabase()

    def getDatabase(self):
        with open("database.json", "r", encoding='utf-8') as read_file:
            self.database = json.load(read_file)
            print(f'Всего юзеров в базе: {self.database["totalUsers"]}')
        self.totalUsers = self.database["totalUsers"]
        self.curDate = self.database["curDate"]
        self.userList.clear()
        for i in range(0, len(self.database["userList"])):
            bufUser = self.database["userList"][i]
            self.userList.append(self.User(bufUser["userName"], bufUser["chatId"], bufUser["boardsList"], bufUser["tagsList"]))
        #self.saveBase()
        return self.database
    
    def addUser(self, newUser):
        for i in range(0, len(self.userList)):
            if newUser.chatId == self.userList[i].chatId:
                return 'Уже зареган'
        self.userList.append(self.User(newUser.userName, newUser.chatId, newUser.boardsList, newUser.tagsList))
        res = self.saveBase()
        if res == 1: return '+1 ПадПищек'
        return 'Ошибка сохранения профиля, обратитесь к @Miku_Tyan, чтобы разрулить проблему'

    def findUser(self, id):
        for i in range(0, len(self.userList)):
            if id == self.userList[i].chatId:
                return i
        return -1

    def reloadUser(self, id, ops, target):
        num = self.findUser(id)
        if ops == 'board':
            buf = self.userList[num].addBoard(target)
            res = self.saveBase()
            if res == 1: return buf
            return 'Ошибка сохранения профиля, обратитесь к @Miku_Tyan, чтобы разрулить проблему'
        if ops == 'tag':
            buf = self.userList[num].addTag(target)
            res = self.saveBase()
            if res == 1: return buf
            return 'Ошибка сохранения профиля, обратитесь к @Miku_Tyan, чтобы разрулить проблему'
        
    def sendProfile(self, id):
        boards = ''
        tags = ''
        num = self.findUser(id)
        if num == -1:    return 'Ты не подписан на рассылку, профиля не существует'
        user = self.userList[self.findUser(id)]
        for i in range(0, len(user.boardsList)):
            boards += f'{user.boardsList[i]}, '
        boards = boards.rstrip(', ')
        for i in range(0, len(user.tagsList)):
            tags += f'{user.tagsList[i]}, '
        tags = tags.rstrip(', ')
        return f'Профиль пользователя {user.userName}:\nID: {user.chatId}\nТвои борды: {boards}\nТвои теги: {tags}'
        

    def saveBase(self):
        updTime = time.asctime()
        self.curDate = updTime
        self.totalUsers = len(self.userList)
        if len(json.dumps(self.compileToModel().dict(), indent = 4, ensure_ascii = False)) > 0:
            with open('database.json', 'w', encoding='utf-8') as write_file:
                json.dump(self.compileToModel().dict(), write_file, indent = 4, ensure_ascii = False)
                print('База обновлена')
                return 1
        else: return 0
        

    def compileToModel(self):
        bufUList = list()
        for i in range(0, len(self.userList)):
            buf = UserModel(userName=self.userList[i].userName, chatId=self.userList[i].chatId, boardsList=self.userList[i].boardsList, tagsList=self.userList[i].tagsList)
            bufUList.append(buf)
        return DatabaseModel(totalUsers = self.totalUsers, curDate = self.curDate, userList = bufUList)

    def convertDBtostr(self, dbModel):
        return json.dumps(dbModel.dict(), indent = 4, ensure_ascii = False)