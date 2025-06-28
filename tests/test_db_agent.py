import unittest
import os
from injector import Injector
from app.services.service import AppModule
from app.agency.pm.pm_agent import PmAgent
from app.db import TasksRepository
from agents import Runner, RunResult

class TestDbAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure MONGODB_URI is set for testing
        if not os.getenv('MONGODB_URI'):
            # You might want to use a dedicated test database URI here
            os.environ['MONGODB_URI'] = 'mongodb://localhost:27017/test_db'

    def setUp(self):
        self.injector = Injector(AppModule)
        self.pm_agent = self.injector.get(PmAgent)
        self.tasks_repo = self.injector.get(TasksRepository)
        # Clear the collection before each test to ensure a clean state
        self.tasks_repo._collection.delete_many({})

    # def tearDown(self):
        # Clean up after each test
        # self.tasks_repo._collection.delete_many({})

    def test_check_tasks_board_with_real_db(self):
        # Insert a dummy task
        dummy_task = {
            "task_id": "test_task_123",
            "description": "This is a test task",
            "status": "pending"
        }
        self.tasks_repo.upsert_task(dummy_task)

        # Call the tool through the agent
        # The agent will decide to call check_tasks_board based on the prompt
        result: RunResult = Runner.run_sync(self.pm_agent, "Check the tasks board for pending tasks")

        # Verify the task exists in the DB after the agent's potential interaction
        # This is the core assertion for this integration test.
        found_tasks = self.tasks_repo.get_tasks(status="pending")
        self.assertTrue(any(t["task_id"] == dummy_task["task_id"] for t in found_tasks))

if __name__ == '__main__':
    unittest.main()
