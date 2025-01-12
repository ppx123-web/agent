from ..agent import Agent
from ..context import LLMMessage, Context
from lambdai import AI

class ChatAgent(Agent):
    name: str = "chat"
    description: str = "An agent that can chat with the user messages."

    def __init__(self):
        super().__init__("chat.j2")

    def run(self, task: str, msg: Context):
        prompt = self.template.render(
            task=task,
            context=str(msg),
        )
        with AI:
            res: str = AI.query(prompt)
            return res