from ..agent import Agent
from ..context import Context
from ..dify import chat_message


class ThinkAgent(Agent):
    description = "Think Agent can only think the task, \
        but it can use better system prompt and \
        return more accurate result. \
        Only user is not satisfied with the previous result, \
        and ask you to re-think the task, \
        This agent will be used."
    
    def __init__(self):
        super().__init__("think.j2")

    def run(self, task: str, msg: Context):
        return chat_message(
            f"The context is: {msg}"
            f"The task is: {task}"
            f"Please think the task and return the result."
        )