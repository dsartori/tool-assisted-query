from setuptools import setup, find_packages

setup(
    name="tool-assisted-query",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "qwen-agent",
        "python-dateutil",
        "python-dotenv",
        "mcp"
    ],
    entry_points={
        'console_scripts': [
            'tool-query = tool_assisted.tool_assisted_query:main'
        ]
    }
)
