import unittest
from agent.myagents.search import SearchAgent
from agent.context import Context

class TestSearch(unittest.TestCase):
    def test_search(self):
        search = SearchAgent()
        result = search.run("Xbox", Context())
        print(result)

if __name__ == "__main__":
    unittest.main()