from setuptools import setup

setup(
    name="daybook",
    version="0.1.2",
    description="URL hoarder's helper utility",
    url="https://github.com/salmiakki/daybook",
    author="Lesha Pak",
    author_email="kapahel@gmail.com",
    packages=["daybook"],
    zip_safe=False,
    install_requires=[
        "loguru>=0.5.3",
        "python-dotenv>=0.17.1",
    ],
    entry_points={
        "console_scripts": ["daybook=daybook.daybook:main"],
    },
)
