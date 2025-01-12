from agent.agent import Agent
from agent.context import Context, LLMMessage
from lambdai import AI

class CodeAgent(Agent):
    def __init__(self):
        super().__init__("code.j2")

    def run(self, task: str, msg: Context):
        prompt = self.template.render(
            context=str(msg),
            task=task,
        )
        with AI:
            res: str = AI.query(prompt)
            return res