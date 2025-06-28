import unittest

from agents import Runner, RunResult
from injector import Injector
from app import AppModule
from app.agency.pm.pm_agent import Agent, PmAgent

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAgents(unittest.TestCase):
    def setUp(self):
        self.injector = Injector(AppModule)

    def test_pm_agent(self):
        pm_agent = self.injector.get(PmAgent)
        result: RunResult = Runner.run_sync(pm_agent, "who was the first president of the united states?")
        logging.info(f"PM Agent Result: {result.final_output_as(str)}")
        self.assertIn("George Washington", result.final_output_as(str), "Expected answer to contain 'George Washington'")

    def test_how_agent_do_nothing(self):
        how_agent = self.injector.get(PmAgent)
        result: RunResult = Runner.run_sync(how_agent, "Call the tool that does nothing")
        logging.info(f"How Agent Result: {result.final_output_as(str)}")

