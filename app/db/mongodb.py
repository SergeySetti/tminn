from injector import inject
from pymongo import MongoClient

MESSAGES_COLLECTION = 'messages'
TASKS_COLLECTION = 'messages'


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

    def get_messages(self, status=None, limit=100, offset=0, from_id=None, to_id=None):
        pass

    def upsert_message(self, message: dict):
        pass

    def gets_tasks(self, status=None, limit=100, offset=0, from_id=None, to_id=None):
        pass

    def upsert_task(self, task: dict):
        pass
