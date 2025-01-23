from lambdai import AI
import unittest

class TestPlan(unittest.TestCase):
    def test_plan(self):
        with AI:
            plan: list[tuple[str, str]] = AI.query(
                "请帮我写一个hello world的程序"
            )



if __name__ == "__main__":
    unittest.main()