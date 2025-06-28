from injector import inject

from .mongodb import Db, MESSAGES_COLLECTION


class MessagesRepository:
    @inject
    def __init__(self, db: Db):
        self._collection = db.get_collection(MESSAGES_COLLECTION)

    def get_message(self, text):
        query = {'text': text}
        message = self._collection.find_one(query)
        return message

    def get_messages(self, status=None, limit=100, offset=0, from_user=None, to_user=None):
        query = {}
        if status is not None:
            query['status'] = status
        id_query = {}
        if from_user is not None:
            id_query['$gte'] = from_user
        if to_user is not None:
            id_query['$lte'] = to_user
        if id_query:
            query['_id'] = id_query
        cursor = self._collection.find(query).skip(offset).limit(limit)
        return list(cursor)

    def upsert_message(self, message):
        if '_id' in message:
            self._collection.replace_one({'_id': message['_id']}, message, upsert=True)
            return message['_id']
        result = self._collection.insert_one(message)
        return result.inserted_id
