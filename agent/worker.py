from queue import Queue
from .agent import Agent
from .context import Context
from .context import LLMMessage
from .dashboard import dashboard
from loguru import logger
from .leader import Leader

class Worker:
    def __init__(self, max_steps: int = 10):
        self.queue: Queue[tuple[Agent, str, Context]] = Queue()
        self.max_steps = max_steps
        self.step = 0
        self.leader = Leader()
    def run(self):
        length = min(self.max_steps, self.queue.qsize())
        with dashboard.show_spinner("Worker is working...") as progress:
            task_id = progress.add_task("Starting work...", total=length)
            
            while self.step < self.max_steps and not self.queue.empty():
                agent, task, msg = self.queue.get()

                progress.update(
                    task_id,
                    description=f"Step {self.step + 1}/{length}: {agent.__class__.__name__} - {task[:60]}..."
                )
                res = agent.run(task, msg)
                
                logger.info(
                    f"Step {self.step + 1}/{length}: {agent.__class__.__name__}: Input\n" + f"{task}".replace("{", "{{").replace("}", "}}"),
                    agent=agent.__class__.__name__
                )
                logger.info(
                    f"Step {self.step + 1}/{length}: {agent.__class__.__name__}: Output\n" + f"{res}".replace("{", "{{").replace("}", "}}"),
                    agent=agent.__class__.__name__
                )
                msg.append(LLMMessage(role="user", content=task))
                msg.append(LLMMessage(role="assistant", content=res))
                is_finished = self.leader.run(msg, task, res)
                if is_finished:
                    self.queue.task_done()
                    self.step += 1
                    progress.advance(task_id)
                else:
                    logger.info(
                        f"Step {self.step + 1}/{length}: {agent.__class__.__name__}: Not finished, fix and retry", agent=self.leader.__class__.__name__
                    )
                    remaining_tasks = []
                    while not self.queue.empty():
                        remaining_tasks.append(self.queue.get())

                    self.queue.put((agent, task, msg))
                    for t in remaining_tasks:
                        self.queue.put(t)



worker = Worker(10)
