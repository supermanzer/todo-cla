import setuptools

with open("README.md", "r") as ld:
    long_description = ld.read()

setuptools.setup(
    name="todo_catalog",
    version="0.2.5",
    description="A command line application used to generate a TODO.md file for a given project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/supermanzer/todo-cla",
    author="C. Ryan Manzer",
    author_email="ryan.manzer@gmail.com",
    packages=["todo_catalog"],
    install_requires=[
        "Click",
        "configparser",
    ],
    entry_points="""
        [console_scripts]
        todo_catalog=todo_catalog.todo_catalog:find_todos
    """,
)
