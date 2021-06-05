import json
import sys

def getDatabase():
    with open("database.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
        print(f'Всего юзеров в базе: {data["totalUsers"]}')
        return data

getDatabase()