from injector import inject
from pymongo import MongoClient

MESSAGES_COLLECTION = 'messages'
TASKS_COLLECTION = 'tasks'


class Db:
    @inject
    def __init__(self, client: MongoClient):
        self.client = client
        self.db = self.client['tminn']

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def get_db(self):
        return self.db

    def get_client(self):
        return self.client

