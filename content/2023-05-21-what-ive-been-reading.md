+++
title = "What I've been reading"
+++

This is a quick post to shout out about things I've been reading that I think
are pretty interesting. Touching on writing Python like Rust, multiple
interpreters with Python 3.12 and cool stuff with Django 4.2.

<!-- more -->

## [Real Multithreading is Coming to Python - Learn How You Can Use It Now](https://martinheinz.dev/blog/97) - Martin Heinz

First up was this really interesting article from Martin
Heinz on the coming "Per-interpreter GIL" (Global Interpreter lock) that is
coming in Python 3.12. The GIL is a restriction within the Python language that
prevents true multi-threading, it enforces that only one thread can be in
control of the Python interpreter at a time. This often leads us to reach for
[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing)
for running code across multiple processors. This model doesn't spawn threads
but rather creates new subprocesses that side-step the GIL and allow us to run
code in parallel. This has a number of disadvantages compared to true
multi-threading, the biggest one which I've seen in the wild is processes don't
share memory like threads so by creating multiple processes you essentially copy
the data you need for each process. In a HPC context this can be a significant
problem because often you want to crunch a big dataset across multiple cores but
you have to use more memory than the actual size of your dataset because you
have to make copies of the data when using `multiprocessing`.

What Martin digs into in his post is how the coming "Per-interpreter GIL" change
in Python 3.12 can actually be used to do true multi-threading! He notes
crucially that this change coming in Python 3.12 isn't for end users and that a
more user friendly version (if the [PEP](https://peps.python.org/pep-0554/) is
accepted) will arrive in 3.13. But this is still a really interesting
development and worth poking if you're interested in high performant Python code.


## [Writing Python like its Rust](https://kobzol.github.io/rust/python/2023/05/20/writing-python-like-its-rust.html) - Jakub Beránek 



## [Writing a chat application in Django 4.2 using async StreamingHttpResponse, Server-Sent Events and PostgreSQL LISTEN/NOTIFY](https://valberg.dk/django-sse-postgresql-listen-notify.html) - Víðir Valberg Guðmundsson

