from agents import Agent
from injector import inject

from app.agency.pm.tools import check_tasks_board

class PmAgent(Agent):
    @inject
    def __init__(self):
        super().__init__(
            name = "pm_agent",
            tools = [check_tasks_board],
        )
