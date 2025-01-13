from ..agent import Agent
from ..context import Context

class FileAgent(Agent):
    description = "File Agent can read, write, and copy files."
    def __init__(self):
        super().__init__("file.j2")

    def run(self, task: str, msg: Context):
        assert False, "File Agent is not implemented."