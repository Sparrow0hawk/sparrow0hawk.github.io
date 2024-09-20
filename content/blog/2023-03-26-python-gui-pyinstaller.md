Title: TWIL: PyInstaller and PySimpleGUI

# TWIL: PyInstaller and PySimpleGUI

Or rather last week I learned...

Recently I’d been asked about a tool I wrote to automate some post processing I do to get files read for mail merges. This was a series of Python scripts I’d written up into a Click command line interface (CLI) package.

<!-- more -->

It’s a cute little pet project that I’d used to learn a bit about [Click](https://click.palletsprojects.com/en/8.1.x/), [mkdocs](https://www.mkdocs.org/) and more modern python packaging ideas ([pyproject.toml](https://peps.python.org/pep-0518/)). One of the many things where Python has made my life a little easier and as such I’ve mentioned it a few times to people who do the same processes. 

However, when it comes to sharing the tool with people who aren’t developers I realised I had a problem. Walking through with someone how to use a command line tool who’s only ever interacted with graphical applications has a whole series of hurdles (it’s a whole lot of new territory to cover for a beginner just to use my tool).  The solution here felt simple, plug the tool into a graphical user interface (GUI). That isn’t something I’d done in Python before but has a vague awareness of the options. With some time to hand and this new incentive to learn I thought I’d give it a shot!

Now there’s plenty of choice when it comes to Python GUI frameworks ([tkinter](https://docs.python.org/3/library/tkinter.html) and [PyQt](https://pypi.org/project/PyQt5/) to name a few). I just needed something simple to get stuck in so I stumbled upon [PySimpleGUI](https://www.pysimplegui.org/en/latest/) which aims to transform existing GUI frameworks into a simple interface. Sounded like what I was after so here we go! 

PySimpleGUI looks at using basic Python structures like lists and dictionaries to organise the GUI interface and events model. This felt ideal, let’s build a simple app.py script that has some fields to capture the input to my CLl, and fire off the CLI with these arguments when clicking a “Run” button. The PySimeplgui website has plenty of existing examples which makes cobbling together my GUI from existing boilerplate nice and straightforward. 

Having the GUI interact with my existing Click CLI logic was the next challenge. Click operates through decorators that you add to commands and sub commands which mean you can’t just import the CLI logic. Conveniently, I read that you can however import a function decorated as a [`Click.Command`](https://click.palletsprojects.com/en/8.1.x/api/#click.Command) and use the [`.callback`](https://click.palletsprojects.com/en/8.1.x/api/#click.Command.callback) function to use the defined Click command within a Python script with the same arguments as specified in the CLI. Perfect. So I can write a GUI that operates with the same logic as the CLI without any duplication! Excellent!

Armed with a working GUI app that behaves the same as my CLI app I now needed to understand how to bundle this all up to provide a single executable for my user. Again this is territory I’m not used to, I’ve written code to run in the command line or for users with existing experience using scripts and code but bundling that all up into a single executable in Python, that’s a new one on me. Enter PyInstaller. PyInstaller is a project I’ve been aware of for some time (I’ve recommended it to some people at work before) but not actually needed to ever use, until now.

[PyInstaller](https://pyinstaller.org/en/stable/) will bundle up a Python script into a single folder (or single file) which captures the scripts dependencies (including a copy of the Python interpreter, but not system libraries) and bundles them all up. It isn’t (annoyingly) a cross compiler so sorting this out cross-OS isn’t straight forward. But as a starter for 10 this would do. Getting started with this is as simple as the command: `pyinstaller your_program.py`.

Initially I wasn’t sure how this would behave with my custom package but was pleasantly surprised to find it behaved just fine. I found this is because PyInstaller is aware of egg installed Python packages so as long as my CLI package is installed with `pip install .` It’s all fine.

