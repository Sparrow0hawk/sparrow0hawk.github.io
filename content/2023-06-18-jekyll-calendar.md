+++
title = "Making a calendar website with Jekyll and GitHub pages"
+++

Recently, I've been working on a Jekyll-based GitHub pages site that presents a
paginated list of upcoming events. It also builds on the [CodeRefinery
git-calendar](https://github.com/coderefinery/git-calendar) tool to generate
and host ICalendar files to enable people to subscribe calendar apps to it. It's
been an interesting look at inverting some of Jekyll's normal logic for blog
posts and using GitHub actions to build markdown posts from YAML.

<!-- more -->

## But why?

I've been a trustee for the [Society of Research Software Engineering](https://society-rse.org/) since
September 2022 and have been working on the communications and publicity front
predominantly. One thing I found is that whilst we have a fantastic Slack space
where people regularly post about events, we don't have a central calendar that
allows people to see all these events in one place.

I stumbled upon the [CodeRefinery
git-calendar](https://github.com/coderefinery/git-calendar) project a few months
ago and thought it was really cool! You could specify your list of events in
YAML and use their tool to generate a simple HTML page and some associated
ICalendar files with your events in. This seemed like a nice solution to my
problem, we could have research software engineers (RSE) contribute their events
into a YAML file and build a calendar file from there!

But I thought, wouldn't it be nice if we could also display these events on a
web page. Now, I've messed around with GitHub pages and Jekyll before so I knew that
Jekyll allowed you to use YAML files as data to populate pages, so I figured
maybe I could pull data from this calendar YAML file into a GitHub pages site as
well as build an ICalendar file from it.

This led to what I described as the [_data
model](https://github.com/Sparrow0hawk/rse-calendar/releases/tag/v0.1.0) for
this calendar website. And this by and large worked, it allowed me to create a
single home page using Jekyll, the minima theme and GitHub pages that populated
a list of events and their associated metadata. What I realised however was that
I couldn't implement nice pagination with this model because of limitations with
how Jekyll pagination behaves, my best approach for getting nice pagination was
to change the model of my site to using posts.

## Inverting the Jekyll blog logic

Jekyll out-of-the-box makes it easy for you to write a blog using their tool.
You have a `_posts` directory and you write your markdown-based blog posts and
pop them in their and it turns them into lovely looking blog pages. That's how
we did blog posts as [Research Computing at the University of
Leeds](https://arc.leeds.ac.uk/blog/) and it works very nicely including support
for pagination.

Pagination, or splitting posts across multiple pages was something I definitely
wanted for the calendar site as its not particularly nice scrolling down one
enormous page of events (assuming I got an enormous number of event submissions
of course). However, Jekyll doesn't support pagination with anything other than
posts and whilst there is a
[jekyll-paginate-v2](https://github.com/sverrirs/jekyll-paginate-v2) gem it
still didn't allow you to do pagination with anything other than things like
posts.

So if I really wanted pagination (and I did) I had to look at a different model
for populating the website event data. In particular I had to find a way to turn
the events in the YAML file into markdown posts. Enter GitHub actions...

## GitHub actions 

To solve my issue of converting YAML data to markdown I fell back to my old
trusty friend Python and more specifically the
[Jinja](https://jinja.palletsprojects.com/en/3.1.x/) templating tool. I could
write a template markdown file that could be populated from a YAML file using
Jinja and just write these files into the `_posts` directory. I could do all
this in Python and use GitHub actions to do this only at site build time.

This was perfect, so 

## Codeless contributions
