from abc import ABC, abstractmethod
from dashboard import dashboard
from dify import chat_message
from lambdai import AI, deepseek_chat
from context import history

tool_list = [
    "direct: the message can be responded or reasoned without using any tools",
    "code: the message can be responded by code, and write code to solve the message."
    "Calculate, or some actions (Send email, search web, etc.) can be done by python code, you should use code tool to do it."
]

ReAct_prompt = f"""
You are an helpful assistant, you can use the following tools to help you answer the question:
{tool_list}
You are as a part of the following workflow:
Flow:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, a tool name or no action
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""



class Work(ABC):
    def __init__(self, name: str, indent: int = 0):
        self.name = name
        self.indent = indent

    @abstractmethod
    def run(self, prompt: str):
        pass

class Question(Work):
    def run(self, prompt: str):
        with dashboard.show_spinner("Question", indent=self.indent) as progress:
            progress.add_task("", total=None)
        history.append(f"Question: {prompt}")
        return Reasoning("Reasoning", self.indent).run(prompt)


class Reasoning(Work):
    def run(self, prompt: str):
        with dashboard.show_spinner("Reasoning", indent=self.indent) as progress:
            progress.add_task("", total=None)
            with AI(config=deepseek_chat):
                response = AI.query(
                    ReAct_prompt + 
                    "You are a Thought stage, you should think about what to do."
                    "Only Complete the Thought stage, do not return any other information."
                    "If the question be solved by python code, then do not directly return the answer, but return the analysis of the question."
                    "Current stage is:"
                    f"{str(history)}\n"
                    "Thought: "
                )
        history.append(f"Thought: {response}")
        return Action("Action", self.indent).run(prompt)


class Action(Work):
    def run(self, prompt: str):
        with dashboard.show_spinner("Action") as progress:
            progress.add_task("", total=None)
            with AI(config=deepseek_chat):
                tool_name: str = AI.query(
                    ReAct_prompt + 
                    "You are a Action stage, you should select the best tool you can use to response the message, and only return the tool name"
                    "The tools are listed below:"
                    "direct: the message can be responded or reasoned without using any tools"
                    "code: the message can be responded by code, and write code to solve the message."
                    "Calculate, or some actions (Send email, search web, etc.) can be done by python code, you should use code tool to do it."
                    "final: the current context contains the final answer, then return the final answer in python code and don not return any other tool name."
                    "The Current Context is:"
                    "\n{}\n"
                    "Select the best tool you can use to response the message, and only return the tool name.",
                    str(history),
                )

        history.append(f"Action: {tool_name}")
        if tool_name == "direct":
            return Reasoning("Direct", self.indent).run(prompt)
        elif tool_name == "code":
            return CodeAction("Code", self.indent).run(prompt)
        elif tool_name == "final":
            return FinalAnswer("FinalAnswer", self.indent).run(prompt)
        else:
            assert False, f"Unknown tool: {tool_name}"

class CodeAction(Work):
    def run(self, prompt: str):
        with dashboard.show_spinner("Code", indent=self.indent) as progress:
            progress.add_task("", total=None)
            with AI(config=deepseek_chat):
                code: str = AI.query(
                    ReAct_prompt + 
                    "You are an Action Input stage, you should generate the python code to solve the question."
                    "Context: \n" + f"{str(history)}\n"
                    "Please return the python code."
                )
                res = AI.query(
                    ReAct_prompt + 
                    "You are an Action Observation stage, you should execute the code and return the result."
                    "Context: \n" + f"{str(history)}\n"
                    "code: \n" + f"{code}\n"
                )
        history.append(f"Observation: {res}")
        return Reasoning("Code", self.indent).run(prompt)
    
class FinalAnswer(Work):
    def run(self, prompt: str):
        with dashboard.show_spinner("FinalAnswer", indent=self.indent) as progress:
            progress.add_task("", total=None)
            with AI(config=deepseek_chat):
                response = AI.query(
                    ReAct_prompt + 
                    "Context: \n" + f"{str(history)}\n"
                    "If the context is enough(contains the answer),"
                    "you should directly answer the question according to the context (return the answer in string in python code)."
                )
        history.append(f"FinalAnswer: {response}")
        return response
