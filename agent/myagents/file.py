from ..agent import Agent
from ..context import Context
from lambdai import AI

class FileAgent(Agent):
    description = "File Agent can read, write files. \
        FileAgent task receives file path, file content and operation described in the task.\
        Then do the operation. \
        The task either is for a absolute path or a relative path for current working directory. \
        If the task is for a relative path, you should change the current working directory to the relative path before using FileAgent."
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