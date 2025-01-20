from .agent import Agent
from .context import Context
from .context import LLMMessage
from .dashboard import dashboard
from loguru import logger
from lambdai import AI
from .client import DeepSeek

# Progress Ledger  
# Task complete® 
# Unproductive loops?  
# Is progress being made®  
# What is the next speaker?   
# Next speaker instruction

class Leader(Agent):
    def __init__(self):
        super().__init__('leader.j2')
        
    def run(self, context: Context, task, res):
        prompt = self.template.render(
            context=context, 
            task=task, 
            result=res
        )
        with AI:
            is_finished: bool = AI.query(prompt)
        return is_finished
        