from agents import Agent
from injector import inject

from app.agency.pm import tools
from app.agency.pm.tools import do_nothing, check_tasks_board
from app.db import TasksRepository


class PmAgent(Agent):
    @inject
    def __init__(self, tasks_repo: TasksRepository):
        tools._tasks_repository = tasks_repo  # Set the injected repository
        super().__init__(
            name = "pm_agent",
            tools = [check_tasks_board, do_nothing],
        )