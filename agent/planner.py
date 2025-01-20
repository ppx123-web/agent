from .worker import Worker
from lambdai import AI
from .agent import Agent
from .context import Context
from .client import DeepSeek
from .dashboard import dashboard

class Planner(Agent):
    description = "Planner is the main agent, it can plan the task and execute it."

    def __init__(self):
        super().__init__("planner.j2")
        self.agents: list[Agent] = []
        self.worker = Worker()

    def add_agent(self, agent):
        self.agents.append(agent)

    def run(self, task, msg: Context):
        agents_dict = {a.__class__.__name__: a for a in self.agents}
        prompt = self.template.render(
            agents=[
                (a.__class__.__name__, a.description) for a in self.agents
            ],
            task=task
        )
        with dashboard.show_single_step("Planner is thinking...") as progress:
            progress.add_task("Planner Thinking")
            with AI:
                res: list[tuple[str, str]] = AI.query(prompt)
                for agent, task in res:
                    assert agent in [agent.__class__.__name__ for agent in self.agents]
        dashboard.render_list([f"{agent}: {task}" for agent, task in res])

        for agent, task in res:
            agent_cls = agents_dict.get(agent)
            if agent_cls is None:
                raise ValueError(f"找不到名为 {agent} 的代理")
            self.worker.queue.put((agent_cls, task, msg))

        self.worker.run()

        summary: str = DeepSeek().ask(
            f"""
            Summarize the answer of the task according to the context.
            And return the response of the task.
            Context:
            {msg}

            The task is:
            {task}

            Now, please answer the task:
            """
        )
        return summary
