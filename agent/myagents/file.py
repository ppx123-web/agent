from ..agent import Agent
from ..context import Context
from lambdai import AI

class FileAgent(Agent):
    description = "File Agent can search, read, write files and change current working directory. \
        FileAgent task receives file path, file content and operation described in the task.\
        Then do the operation."
    def __init__(self):
        super().__init__("file.j2")

    def run(self, task: str, msg: Context):
        prompt = self.template.render(
            task=task,
            context=str(msg),
        )
        with AI:
            res = AI.query(prompt)
        return res