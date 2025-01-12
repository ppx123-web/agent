from queue import Queue
from .agent import Agent
from .context import Context
from .context import LLMMessage

class Worker:
    def __init__(self, max_steps: int = 10):
        self.queue: Queue[tuple[str, Agent, Context]] = Queue()
        self.max_steps = max_steps
        self.step = 0

    def run(self):
        while self.step < self.max_steps:
            task, agent, msg = self.queue.get()
            res = agent.run(task, msg)
            msg.append(LLMMessage(role="assistant", content=res))
            self.queue.task_done()
            self.step += 1

worker = Worker(10)
