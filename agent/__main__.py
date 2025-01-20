from .dashboard import dashboard
from lambdai import deepseek_chat
from .planner import Planner
from .myagents.think import ThinkAgent
from .myagents.code import CodeAgent
from .myagents.clear import ClearAgent
from .myagents.file import FileAgent
from .myagents.chat import ChatAgent
from .myagents.shell import ShellAgent
from .myagents.search import SearchAgent
from .myagents.workspace import WorkspaceAgent
from .context import Context, LLMMessage
from loguru import logger


def query(question, msg: Context):
    agent = Planner()
    agent.add_agent(ThinkAgent())
    agent.add_agent(CodeAgent())
    agent.add_agent(ClearAgent())
    agent.add_agent(ChatAgent())
    agent.add_agent(FileAgent())
    agent.add_agent(ShellAgent())
    agent.add_agent(WorkspaceAgent())
    return agent.run(question, msg)

if __name__ == "__main__":
    deepseek_chat.remove_logger()
    deepseek_chat.log_file = "logs/main.log"
    deepseek_chat.log_level = "DEBUG"
    deepseek_chat.apply()

    def log_filter(record):
        return record["extra"].get("agent") is not None

    logger.add(
        "logs/agent.log", mode="w", 
        filter=log_filter
    )

    msg = Context()

    while True:
        try:
            user_input = dashboard.render_input("$ ")
            if user_input:
                result = query(user_input, msg)
                msg.append(LLMMessage(role="assistant", content=result))
                dashboard.render_markdown(str(result))
        except EOFError:
            break
        except KeyboardInterrupt:
            break
