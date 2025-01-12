from jinja2 import Environment, FileSystemLoader
from .client import DeepSeek
from .context import Context


env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=True
)


class Agent:
    name: str = ""
    description: str = ""

    def __init__(self, prompt_file: str):
        self.template = env.get_template(prompt_file)
        self.client = DeepSeek()

    def run(self, task: str, msg: Context):
        pass