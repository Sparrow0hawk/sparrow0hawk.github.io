# What I've been reading

This is a quick post to shout out about things I've been reading that I think
are pretty interesting. Touching on writing Python like Rust, multiple
interpreters with Python 3.12 and cool stuff with Django 4.2.

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

Update: On this point above about processes and memory use, this isn't strictly
true on Linux due to copy-on-write. So when we create multiple processes they
don't actually copy the memory for each process unless they actually try and
change the value. Thanks John Hodrien for pointing this out![1]

What Martin digs into in his post is how the coming "Per-interpreter GIL" change
in Python 3.12 can actually be used to do true multi-threading! He notes
crucially that this change coming in Python 3.12 isn't for end users and that a
more user friendly version (if the [PEP](https://peps.python.org/pep-0554/) is
accepted) will arrive in 3.13. But this is still a really interesting
development and worth poking if you're interested in high performant Python code.


## [Writing Python like its Rust](https://kobzol.github.io/rust/python/2023/05/20/writing-python-like-its-rust.html) - Jakub Beránek 

This post for me managed to capture something I've felt since starting to play
with Rust and having to move back to other languages like R and Python. One of
the best things about Rust is the way it forces you to think differently about
how you'd write other code, and to strive for "correctness" even without the
Rust compiler. I know I'll be referring back to this post for a while!

## [Writing a chat application in Django 4.2 using async StreamingHttpResponse, Server-Sent Events and PostgreSQL LISTEN/NOTIFY](https://valberg.dk/django-sse-postgresql-listen-notify.html) - Víðir Valberg Guðmundsson

I've written some Django stuff in my time but nothing quite as clever as this.
This post looks as some really cool features in Django 4.2 and how you can
integrate these with the Server-side events (SSE) API to building real-time applications. 
This is pushing the envelope in terms of things I thought were do-able with
Django so it's great to have this post that walks through these topics and does
so with plenty of detail.

## [Memory allocation](https://samwho.dev/memory-allocation/) - Sam Rose

This is a fun post looking at memory and memory allocation and how simple
allocators work. As someone not from a computer science background I really love
posts like this that help fill out my understanding of what is actually going on
with things like memory. This post also comes with some great interactive
widgets and cute little dog call outs, whats not to like! 

[1]: https://twitter.com/johnhodrien/status/1662824749930627073
