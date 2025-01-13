import unittest
from agent.planner import Planner
from agent.myagents import ChatAgent
from agent.dashboard import dashboard
from agent.myagents.search import SearchAgent
from agent.myagents.code import CodeAgent

class TestPlanner(unittest.TestCase):
    def test_planner(self):
        planner = Planner()
        agent = ChatAgent()
        code = CodeAgent()
        planner.add_agent(agent)
        planner.add_agent(code)
        result = planner.run("计算213123*564")
        dashboard.render_markdown(result)

if __name__ == "__main__":
    unittest.main()
