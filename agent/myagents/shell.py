from ..agent import Agent
from ..context import Context
from ..context import LLMMessage
from ..dashboard import dashboard
from loguru import logger
import os
from lambdai import AI


class ShellAgent(Agent):
    def __init__(self):
        super().__init__('shell.j2')
        self.description = "Shell Agent can receive a task and use shell command to execute it. But it cannot change the current working directory."

    def run(self, task: str, msg: Context) -> str:
        prompt = self.template.render(task=task, context=str(msg))
        with AI:
            cmd = AI.query(prompt)
        
        try:
            exit_code = os.system(cmd)
            if exit_code == 0:
                res = f"{task}执行成功: {cmd}"
                logger.info(f"命令执行成功: {task} - {cmd}")
            else:
                res = f"{task}执行失败: {cmd}"
                logger.error(f"命令执行失败: {task} - {cmd}")
                
        except Exception as e:
            res = f"{task} 执行命令 {cmd} 时发生错误: {str(e)}"
            logger.error(f"执行命令异常: {task} - {cmd} - {str(e)}")
        return res