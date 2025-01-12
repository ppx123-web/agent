from ..agent import Agent
from ..context import LLMMessage, Context
from ..client import DeepSeek

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
        res = DeepSeek().ask(prompt)
        return res