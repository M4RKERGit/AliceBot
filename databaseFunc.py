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
                    self.boardsList = self.tagsList.pop(i)
                    return f'Борда {recBoard} удалена из твоего списка'
            self.boardsList.append(recBoard)
            return f'Борда {recBoard} добавлена в твой список'


        def addTag(self, recTag):
            for i in range(0, len(self.tagsList)):
                if recTag == self.tagsList[i]:
                    self.tagsList = self.tagsList.pop(i)
                    return f'Тег {recTag} удален из твоего списка'
            self.boardsList.append(recTag)
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
        self.saveBase()
        return '+1 ПадПищек'

    def findUser(self, id):
        for i in range(0, len(self.userList)):
            if id == self.userList[i].chatId:
                return i
        return -1

    def reloadUser(self, id, ops, target):
        num = self.findUser(id)
        if ops == 'board':
            self.userList[num].addBoard(target)
        if ops == 'tag':
            self.userList[num].addTag(target)

    def saveBase(self):
        updTime = time.asctime()
        self.curDate = updTime
        self.totalUsers = len(self.userList)
        with open('database.json', 'w', encoding='utf-8') as write_file:
            json.dump(self.compileToModel().dict(), write_file, indent = 4, ensure_ascii = False)
            print('База обновлена')

    def compileToModel(self):
        bufUList = list()
        for i in range(0, len(self.userList)):
            buf = UserModel(userName=self.userList[i].userName, chatId=self.userList[i].chatId, boardsList=self.userList[i].boardsList, tagsList=self.userList[i].tagsList)
            bufUList.append(buf)
        return DatabaseModel(totalUsers = self.totalUsers, curDate = self.curDate, userList = bufUList)

    def convertDBtostr(self, dbModel):
        return json.dumps(dbModel.dict(), indent = 4, ensure_ascii = False)