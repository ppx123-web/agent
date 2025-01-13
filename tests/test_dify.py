from agent.dify import chat_message
import unittest

class TestDify(unittest.TestCase):
    def test_chat_message(self):
        res = chat_message("What is XBox?")
        print(res)


if __name__ == "__main__":
    unittest.main()
