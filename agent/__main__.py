from .dashboard import dashboard
from lambdai import deepseek_chat
from .planner import Planner
from .myagents.think import ThinkAgent
from .myagents.code import CodeAgent
from .myagents.clear import ClearAgent
from .myagents.file import FileAgent
from .myagents.chat import ChatAgent
from .myagents.search import SearchAgent
from .context import Context, LLMMessage
# 1. routing
# 2.1 research question
# 2.2 programming question
# 3. RAG Search: 爬虫Search & Cot Agent
# 4. table data processing
# 5. chat
# 6. personlized extension: extend serveral single words to a clear problem according to the context: named pe


# dify
#   API workflow & chat call

# tool pool


'''

1. stage design
'''

def query(question, msg: Context):
    agent = Planner()
    agent.add_agent(ThinkAgent())
    agent.add_agent(CodeAgent())
    agent.add_agent(ClearAgent())
    agent.add_agent(ChatAgent())
    return agent.run(question, msg)

if __name__ == "__main__":
    deepseek_chat.remove_logger()
    deepseek_chat.log_file = "logs/main.log"
    deepseek_chat.log_level = "DEBUG"
    deepseek_chat.apply()

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
