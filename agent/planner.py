from .worker import Worker
from lambdai import AI
from .agent import Agent
from .context import Context
from .client import DeepSeek
from .dashboard import dashboard
from loguru import logger

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
        plan = self.plan(task)

        error_msg = None
        while True:
            self.render_plan(plan)
            advice = self.get_advice()
            if advice:
                # need to replan
                with dashboard.show_single_step("RePlanner is thinking...") as progress:
                    progress.add_task("RePlanner Thinking")
                    plan = RePlanner().run(advice, self.agents, plan, error_msg)
                error_msg = None
                continue
            # directly execute
            for agent, task in plan:
                agent_cls = agents_dict.get(agent)
                if agent_cls is None:
                    raise ValueError(f"找不到名为 {agent} 的代理")
                self.worker.queue.put((agent_cls, task, msg))

            try:
                self.worker.run()
            except Exception as e:
                logger.error(f"执行任务时发生错误: {e}, 重新规划任务")
                error_msg = str(e)
                continue
            return self.summary(task, msg)
    
    def summary(self, task: str, msg: Context) -> str:
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

    def plan(self, task: str) -> list[tuple[str, str]]:
        prompt = self.template.render(
            agents=[
                (a.__class__.__name__, a.description) for a in self.agents
            ],
            task=task
        )
        with dashboard.show_single_step("Planner is thinking...") as progress:
            progress.add_task("Planner Thinking")
            with AI:
                plan: list[tuple[str, str]] = AI.query(prompt)
                for agent, task in plan:
                    assert agent in [agent.__class__.__name__ for agent in self.agents]
        return plan
    
    def get_advice(self) -> str:
        confirm = dashboard.render_confirm("Do you want to execute the task?[Y/N]")
        if confirm:
            return None
        else:
            advice = dashboard.render_input("Your advice: ")
            return advice

    def render_plan(self, plan: list[tuple[str, str]]):
        dashboard.render_list([f"{agent}: {task}" for agent, task in plan])

class RePlanner(Agent):
    description = "RePlanner is one of the main agent, it can replan the task according to the previous plan."

    def __init__(self):
        super().__init__("replanner.j2")

    def run(self, requirement: str, agents: list[Agent], tasks: list[tuple[str, str]], error_msg: str):
        prompt = self.template.render(
            requirement=requirement,
            agents=[(a.__class__.__name__, a.description) for a in agents],
            tasks=tasks,
            error_msg=error_msg
        )
        with AI:
            res: list[tuple[str, str]] = AI.query(prompt)
        return res
