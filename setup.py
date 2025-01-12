from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agent",
    version="0.1.0",
    description="An agent-based system with planning capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "jinja2",  # 用于模板渲染
        "pytest",  # 用于测试
    ],
    package_data={
        "agent": ["templates/*.j2"],  # 包含模板文件
    },
    entry_points={
        "console_scripts": [
            "agent=agent.dashboard:main",  # 命令行入口点
        ],
    },
) 