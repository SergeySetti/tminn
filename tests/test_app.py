import unittest

from injector import Injector

from app import AppModule
from app.db import Db, MessagesRepository, TasksRepository


class TestDependencyInjection(unittest.TestCase):
    def setUp(self):
        self.injector = Injector(AppModule)

    def test_home_page(self):
        from app import create_app
        app = create_app()
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_messages_repository(self):
        messages_repository: MessagesRepository = self.injector.get(MessagesRepository)
        self.assertIsNotNone(messages_repository)
        # insert a test message
        test_message = {
            'task_id': 'TASK-1',
            'text': 'Test message',
            'sender': 'test_sender',
            'receiver': 'test_receiver'
        }
        messages_repository.upsert_message(test_message)
        # retrieve the message
        retrieved_message = messages_repository.get_message(test_message['text'])
        self.assertIsNotNone(retrieved_message)
        self.assertEqual(retrieved_message['text'], test_message['text'])
        # update the message but keep an _id
        test_message['text'] = 'Updated test message'
        messages_repository.upsert_message(test_message)
        updated_message = messages_repository.get_message(test_message['text'])
        self.assertIsNotNone(updated_message)
        self.assertEqual(updated_message['text'], test_message['text'])

    def test_tasks_repository(self):
        tasks_repo: TasksRepository = self.injector.get(TasksRepository)
        self.assertIsNotNone(tasks_repo)
        # insert a test task
        test_task = {
            'task_id': 'TASK-1',
            'description': 'Test task',
            'status': 'pending',
            'assignee': 'BE-1'
        }
        tasks_repo.upsert_task(test_task)
        # retrieve the task
        retrieved_task = tasks_repo.get_task_by_id(test_task['task_id'])
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task['task_id'], test_task['task_id'])
        # update the task but keep a task_id
        test_task['status'] = 'completed'
        tasks_repo.upsert_task(test_task)
        updated_task = tasks_repo.get_task_by_id(test_task['task_id'])
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['status'], test_task['status'])

