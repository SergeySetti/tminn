from injector import inject

from .mongodb import Db, TASKS_COLLECTION


class TasksRepository:
    @inject
    def __init__(self, db: Db):
        self._collection = db.get_collection(TASKS_COLLECTION)

    def get_task_by_id(self, task_id):
        task = self._collection.find_one({'task_id': task_id})
        if not task:
            raise ValueError(f'Task with task_id {task_id} not found')
        return task

    def get_tasks(self, status=None, limit=100, offset=0, from_id=None, to_id=None):
        query = {}
        if status is not None:
            query['status'] = status
        id_query = {}
        if from_id is not None:
            id_query['$gte'] = from_id
        if to_id is not None:
            id_query['$lte'] = to_id
        if id_query:
            query['_id'] = id_query
        cursor = self._collection.find(query).skip(offset).limit(limit)
        return list(cursor)

    def upsert_task(self, task):
        if 'task_id' in task:
            self._collection.replace_one({'task_id': task['task_id']}, task, upsert=True)
            return task['task_id']
        result = self._collection.insert_one(task)
        return result.inserted_id
