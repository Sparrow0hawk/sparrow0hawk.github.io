+++
title = "Research Security Snippets #2 Secret stuff"
[extra]
author = "Alex Coleman, Samantha Finnigan"
+++

> A big thank you to Samantha Finnigan, RSE from Durham for helping co-author this post
and advice on content

In this instalment of Research Software security snippets, we're going to talk
about secrets! Not those deep and darkest things, but rather all those bits of
information you need in your code for it to run that you don’t want shared with
everyone else.
<!-- more -->

## Secrets and Environments

Let’s start off by defining these secrets. A secret is something like an API key, a
password, username, database key or authentication token that your code uses to
run, but that is a private piece of information you wouldn’t want to share.
Including these secrets publicly in our source code a bad idea. They expose us
to bad actors who could impersonate us to access systems or use APIs we’re
paying for (some of a few potential bad examples). Secret leakage is a major
cause of security incidents at companies: for example, [Uber in 2022 was
breached](https://blog.gitguardian.com/uber-breach-2022/amp/) using hard coded
admin credentials that allowed attackers to breach their privilege access management platform.

Leaking secrets is very easy to do. Often the biggest mistake can be hard coding 
them into our source code and (whilst trying to be good and using version control)
committing this secret-in-source-code into our version history. We might then push 
that to a public repository, and voila(!), our secret is publicly available on our
public source repository! 

Another way that secrets leak is through tools such as Docker. Docker is a
containerisation tool that allows us to bundle software and its dependencies
(including operating system dependencies) into a container we can share with
others. In Docker we might use things like environment variables (more on those
below) to manage secrets that allow our software to connect to a service, like a
database, but these environment variables are still encoded within the container
and anyone  can view them if we make the container publicly available through a
container repository such as [Docker Hub](https://hub.docker.com).

Secrets are a really easy thing to accidentally share when we’re first learning
about using version control tools like git. We’re trying our hardest to keep
things versioned, and accidentally commit a file containing our secret. Once the
file is in our git history it can be difficult/painful to extract it (especially
if we don’t realise this immediately). The first thing to do when using secrets
within our code is to separate them out from our source code. Secrets shouldn’t
live within our code, it’s much better to find a way to inject them when our
code runs. 

## Separating code and secrets: Environment variables

The classic way to do this is with environment variables. Environment
variables are named key/value pairs that exist within the system environment. We can
retrieve the value using the environment variable name because they’re set
outside our program. They have been historically used as a method for storing
secrets which we can retrieve in our code:

```python
# main.py
import os
print(os.environ[“TEST”])
```

```bash
$ export TEST=magic-key
$ python main.py
magic-key
```

From the simplified above example you can hopefully see how you could use
environment variables to store secrets outside of your code but still retrieve
them at run time.

To avoid having to explicitly set all these environment variables before you run
your code there are a number of packages that let you specify a `.env` file
(often called "dotenv") in which you specify your secrets as key-value pairs.
For instance (by not exhaustively), in Python there's
[decouple](https://pypi.org/project/python-decouple), in R you can use the
default [`.Renviron`](https://bookdown.org/content/d1e53ac9-28ce-472f-bc2c-f499f18264a3/envManagement.html#use-.renviron-file)
file. 

This allows you to start to separate your code and your secrets and do so in a
convenient way. Environment variables aren't perfect but they are a good easy
entry point for starting to secure your code.

## Keeping secrets out of the public eye

The `.env` file or `.Renviron` files should never be commited to version
control, but allow you on a project-by-project basis to handle secrets using configuration files. 

The `.gitignore` file is our friend in these situations. If you've used git for
version control you may or may not be familiar with the [`.gitignore`
file](https://git-scm.com/docs/gitignore). Sometimes all we want is to actually
ignore a file from version control and make sure it isn't accidentally added and tracked. 

The `.gitignore` file is just a text file that lives in the root of our repository. 
Each line in the file specifies a pattern of file/folder names to ignore. This
allows us to easily specify specific files or patterns (file extensions) that
should be ignored in our repository. For managing our secrets in a `.env` file,
this means we just add `.env` as a line in our `.gitignore`, and that file won't
be tracked by git, keeping our secrets out of version control. We should commit
the `.gitignore` file into version control, so that cloned versions of our
repository will also ignore the files listed!

Docker provides similar functionality through the `.dockerignore` file.
Accidentally copying `.env` files into our Docker images can be surprisingly
easy, as the following example demonstrates:

```Dockerfile
FROM alpine:latest
COPY . .
CMD ["cat", ".env"]
```

The `COPY . .` command in this Dockerfile was intended to copy our application files, but
has a potentially unforseen side-effect: it will copy dotfiles (files with a dot
in front), too! This includes our `.env` file containing all our secrets:

```bash
$ echo "# THIS FILE SHOULD NOT BE COPIED!" > .env
$ docker build --tag=test .
$ docker run test
# THIS FILE SHOULD NOT BE COPIED!
```

Oops! `.dockerignore` uses exactly the same syntax as `.gitignore`, so an `.env`
file can be easily excluded from the Docker image by commiting a `.dockerignore`
file with the following content into our repository:

```.gitignore
**/*.env
```

Now when we build and run our example container, the `.env` file is not included
by the `COPY . .` command:

```bash
$ docker build --tag=test .
$ docker run test
cat: can't open '.env': No such file or directory
```

However, the downside of environment variables is that they are still plain text
within our system, so if the system our code is running on is compromised bad
actors can still get at our secrets! 

## Oops, I accidentally committed a secret. What now?

We've now learned how to keep secrets out of our Git repositories in the first
place, but what happens if we accidentally commit and push them? It's too easy
for something to slip through the net, despite implementing best practices like `.gitignore` and `.dockerignore`.

Third-party tools like [GitGuardian](https://gitguardian.com/) (free for teams
of 25 members or fewer)  can enable us to take corrective action when the worst
happens. GitGuardian scans repositories against a
set of definitions for known types of secret, and creates an "Incident" where a
match is found. It can even be set up as part of a CI/CD pipeline, and send a
notification to enable us to realise and revoke a leaked secret in real-time.

This links to a key design principle: Secrets should be revokable. We're
familiar with the concept of changing our passwords for online services and
websites, and it's a similar principle. Third-party APIs and services often
employ an API key, so that we don't have to write code which needs access to our
personal password. For example, DockerHub allows us to create API keys which
scripts can use to publish our containers, avoiding the need to provide our CI/CD scripts with a password.

API keys allow us to limit access to an application through the principle of
least privilege. Instead of a password, which allows access to all functions of
an application, an API key often provides the ability to give our applications only the permissions which they require: e.g. read-only access, or access to a
limited set of resources. API keys can be easily revoked, removing the
possibility for them to be used by a malicious actor, and limiting their
permissions can limit or mitigate the damage that can be done if and when they
do leak. API keys can be easily revoked, removing the possibility for them to be used by
a malicious actor, and limiting their permissions can limit or mitigate the
damage that can be done if and when they do leak. However, before revoking an
API key, it's sensible to work out what features of your application rely on it
and may fail when they no longer have permission to access the resource, as this
can cause other problems. When an API key gives few permissions, it may be more
reasonable to create a new key and deploy it to the production environment,
before revoking the compromised secret. 

Tools such as the [BFG repo cleaner](https://github.com/rtyley/bfg-repo-cleaner)
can be used to alter git repository history, for example to remove a
secret-containing file that should never have been committed 
in the first place. In general, this approach should be applied with caution:
never assume that by removing the secret from the repository, it's now gone.
Once something has been published to the internet, for 
however little time, it should be considered compromised. While you can remove
the file from the repository in this way, any leaked API keys also need to be
revoked.

## Conclusion

We've taken some tentative steps above to introduce ideas around code secrets
and how we manage them. Separating our secrets and our code is a key step in
keeping ourselves safe and ensuring our code is secure. Environment variables
are a classic way to do this and widely supported with the concept of "dotenv"
files but aren't perfect. We also touched on how its easy to accidentally
include secrets in version control and within container images and suggest some
tips for how to prevent this using ignore files. In future snippets we'll dig
into some more advanced approaches to managing secrets.

