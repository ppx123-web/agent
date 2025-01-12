import unittest
from agent.planner import Planner
from agent.myagents import ChatAgent
from agent.dashboard import dashboard

class TestPlanner(unittest.TestCase):
    def test_planner(self):
        planner = Planner()
        agent = ChatAgent()
        planner.add_agent(agent)
        result = planner.run("Write python codeto print hello world.")
        dashboard.render_markdown(result)

if __name__ == "__main__":
    unittest.main()
