from queue import Queue
from .agent import Agent
from .context import Context
from .context import LLMMessage
from .dashboard import dashboard
from loguru import logger
class Worker:
    def __init__(self, max_steps: int = 10):
        self.queue: Queue[tuple[Agent, str, Context]] = Queue()
        self.max_steps = max_steps
        self.step = 0

    def run(self):
        length = min(self.max_steps, self.queue.qsize())
        with dashboard.show_spinner("Worker is working...") as progress:
            task_id = progress.add_task("Starting work...", total=length)
            
            while self.step < self.max_steps and not self.queue.empty():
                agent, task, msg = self.queue.get()

                progress.update(
                    task_id,
                    description=f"Step {self.step + 1}/{length}: {agent.__class__.__name__} - {task[:30]}..."
                )
                
                msg.append(LLMMessage(role="user", content=task))
                logger.info(
                    f"Step {self.step + 1}/{length}: {agent.__class__.__name__}: Input\n{task}",
                    agent=agent.__class__.__name__
                )
                res = agent.run(task, msg)
                msg.append(LLMMessage(role="assistant", content=res))
                logger.info(
                    f"Step {self.step + 1}/{length}: {agent.__class__.__name__}: Output\n{res}", 
                    agent=agent.__class__.__name__
                )
                self.queue.task_done()
                self.step += 1

                progress.advance(task_id)

worker = Worker(10)
