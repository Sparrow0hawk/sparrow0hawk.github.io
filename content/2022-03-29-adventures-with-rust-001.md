# Adventures with Rust part 1

I've been interested in learning the [Rust language](https://www.rust-lang.org/) for quite a while. 

It regularly gets voted "Most Loved programming language" in the annual StackOverFlow Developer Survey[^1] and there's an emerging interest within the scientific community[^2].

So a combination of personal and professional curiosity has led me to starting to have a poke around with the language. 
Rust prides itself on it's speed and memory safety through the _borrow checker_ that checks references at compile time, the first of which sounds very nice to me as a python programmer and the second sounds important but isn't something I think about as a python programmer.

Getting started learning Rust has felt quite straightforward with the excellent [Rust book](https://doc.rust-lang.org/book/), the [Rustlings course](https://github.com/rust-lang/rustlings/) and of course [Rust by example](https://doc.rust-lang.org/stable/rust-by-example/).
These are great resources i've started chewing through slowly but as i've found with learning languages previously (and indeed my continuing journey as an R programmer and pythonista) you really learn a language when you start hacking about with your own projects. 

But for me Rust is a very different language from what i'm used to, so i've found it quite difficult to just start tacking together my own projects (especially when my reflex is to start everything in python). 
This led me back around to some things I did in the early days of learning python such as writing a small program to extract [password protected .zip files](https://github.com/Sparrow0hawk/zip_unlock).

This came about because I was once sent a password-protected zip file and a password, but sadly the provided password didn't work! 
I had a hunch this was because there was a single typo somewhere in the provided password so wrote a quick python project that looked to take a password suggestion and through standard brute force techniques create many permutations of the password and try them on the .zip.
It was a small trivial little project that I can honestly say I've used just twice but it was a nice challenge to put me through my paces and apply some of the things i'd learnt about python at the time.

So with the prospect of a reasonably long train journey ahead, last night I set about re-implementing this project in [Rust](https://github.com/Sparrow0hawk/zip-cracker-rs). 

[^1]: https://insights.stackoverflow.com/survey/2021
[^2]: https://www.nature.com/articles/d41586-020-03382-2
