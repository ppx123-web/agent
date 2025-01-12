from jinja2 import Environment, FileSystemLoader
from .client import DeepSeek
from .context import Context
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=True
)


class Agent:
    description: str = ""

    def __init__(self, prompt_file: str):
        self.template = env.get_template(prompt_file)
        self.client = DeepSeek()

    def run(self, task: str, msg: Context):
        pass
