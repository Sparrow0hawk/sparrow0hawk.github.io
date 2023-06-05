+++
title = "Research Security Snippets #2 Secret stuff"
+++

In this instalment of Research Software security snippets I’m going to talk
about secrets! Not those deep and darkest things but rather all those bits of
information you need in your code for it to run that you don’t want shared with
everyone else! 
<!-- more -->
Let’s start off by defining these secrets. A secret something like an API key, a
password, username, database key or authentication token that your code uses to
run but that is a private piece of information you wouldn’t want to share.
Including these secrets publicly in our source code a bad idea. They expose us
to bad actors who could impersonate us to access systems or use APIs we’re
paying for (some of a few potential bad examples). Secret leakage is a major
cause of security incidents at companies, for example Uber in 2022 was breached
using hard coded admin credentials allowing attackers to breach their privilege
access management platform  https://blog.gitguardian.com/uber-breach-2022/amp/ 

Leaking secrets is very easy to do. Often the biggest mistake can be hard coding them into our source code and (whilst trying to be good and using version control) commit this secret-in-source-code into our version history. We might then push that to a public repository and voila our secret publicly available on our public source repository! 
Another way we can leak secrets is through tools such as Docker. Docker is a
containerisation tool that allows us to bundle software and its dependencies
(including operating system dependencies) into a container we can share with
others. In Docker we might use things like environment variables to manage
secrets that allow our software to connect to a service, like a database, but
these environment variable are still encoded within the container and if we make
the container publicly available anyone can view these environment variables. 

Secrets are a really easy thing to accidentally share when we’re first learning
about using version control tools like git. We’re trying our hardest to keep
things versions and accidentally commit a file containing our secret. One the
file is in our git history it can be difficult/painful to extract it (especially
if we don’t realise this immediately). The first thing to do when using secrets
within our code is to separate them out from our source code. Secrets shouldn’t
live within our code, it’s much better to find a way to inject them when our
code runs. The classic way to do this is with environment variables. Environment
variables are named values that exist within the system environment, we can
retrieve the value using the environment variable name because they’re set
outside our program they have been historically used as a method for storing
secrets which we can retrieve in our code. 

```python
import os

print(os.environ[“TEST”])
```

```bash
export TEST=magic-key
python main.py
magic-key
```

From the simplified above example you can hopefully see how you could use
environment variables to store secrets outside of your code but still retrieve
them at run time. 

To avoid having to explicitly set all these environment variables before you run
them there are a number of packages that let you specify a `.env` file in which
you specify your secrets as key-value pairs. In Python there's
[decouple](https://pypi.org/project/python-decouple), in R you can use the
default
[`.Renviron`](https://bookdown.org/content/d1e53ac9-28ce-472f-bc2c-f499f18264a3/envManagement.html#use-.renviron-file)
file. The `.env` file or `.Renviron` files should never be commited to version
control but allow you on a project-by-project basis to
handle secrets using configuration files. 

The .gitignore file is our friend in these situations. If you've used git for
version control you may or may not be familiar with the [`.gitignore`
file](https://git-scm.com/docs/gitignore). Sometimes all we want is to actually
ignore a file from version control and make sure it isn't added and tracked. You
can ignore files and folders easily in git using the `.gitignore`. This is just
a text file that lives in the root of our repository where each line specifies a
pattern of file/folder names to ignore. This allows us to easily specify
specific files or patterns (file extensions) that should be ignored in our
repository. For managing our secrets in a `.env` file this means we just add
`.env` as a line in our `.gitignore` and that file won't be tracked by git,
keeping our secrets out of version control.

However, the downside of environment variables is that they are still plain text within our system so if the system our code is running on is compromised bad actors can still get at our secrets! 


- what is a secret
- How do we leak them?
- Secrets and git
- Secret sprawl survey?
- GitHub secret scanning 
- Secrets and docker/containers
- Tools for managing secrets
- Git hooks
- Dotenv
- Environment variables
- Keyvaults

