from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.live import Live
from rich.layout import Layout
import time

class Dashboard:
    def __init__(self):
        self.console = Console()
    
    def render_input(self, prompt: str = "") -> str:
        """渲染输入提示并获取用户输入"""
        text = Text(prompt, style="bold blue")
        self.console.print(text, end="")
        return input()
        
    def render_text(self, content: str, style: str = None):
        """渲染普通文本"""
        text = Text(content, style=style) if style else Text(content)
        self.console.print(text)
        
    def render_markdown(self, content: str):
        """渲染 Markdown 内容"""
        markdown = Markdown(content)
        self.console.print(markdown)
        
    def render_panel(self, content: str, title: str = "", style: str = "bold blue"):
        """渲染带边框的面板"""
        panel = Panel(
            content,
            title=title,
            style=style,
            border_style="blue"
        )
        self.console.print(panel)
        
    def render_table(self, headers: list, rows: list):
        """渲染表格"""
        table = Table()
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*row)
        self.console.print(table)
        
    def render_error(self, message: str):
        """渲染错误信息"""
        self.console.print(f"[red]错误: {message}[/red]")
        
    def render_success(self, message: str):
        """渲染成功信息"""
        self.console.print(f"[green]成功: {message}[/green]")

    def show_spinner(self, message: str = "思考中...", indent: int = 0):
        """显示加载动画"""
        return Progress(
            TextColumn("[bold blue]" + "    " * indent),
            SpinnerColumn(),
            TextColumn("[bold blue]" + message),
            transient=True
        )
        
    def clear(self):
        """清空控制台"""
        self.console.clear()

dashboard = Dashboard()
