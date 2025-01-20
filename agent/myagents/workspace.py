from ..agent import Agent
from ..context import Context
from lambdai import AI
import os


class WorkspaceAgent(Agent):
    description: str = "Workspace Agent can manage the workspace. It can only change the current working directory."
    def __init__(self):
        super().__init__('workspace.j2')

    def run(self, task: str, msg: Context) -> str:
        prompt = self.template.render(task=task, context=str(msg))
        with AI:
            path = AI.query(prompt)
        try:
            os.chdir(path)
            return f"成功切换到目录: {path}"
        except Exception as e:
            return f"切换目录失败: {e}"
