from ..agent import Agent
from ..context import Context


class ClearAgent(Agent):
    description = "Clear Agent can only clear the context when required."
    def __init__(self):
        super().__init__("clear.j2")

    def run(self, task: str, msg: Context):
        msg.clear()
        return ""