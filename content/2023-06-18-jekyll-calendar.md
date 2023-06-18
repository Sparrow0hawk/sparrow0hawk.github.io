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

## Jekyll blogs and pagination

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
Jinja and just write these files into the `_posts` directory. This would allow
me to avoid duplicating data across the site and also preserve the YAML file
that was used to generate the ICalendar files. 

GitHub actions provides a mechanism why which I can run this Python script to
generate posts only when building the site for deploying to GitHub pages. This
ensures when developing the site I don't create undue duplications between the
calendar data in the YAML file and in any generated posts. I'm still adhering to
the principle of keeping the YAML file as the central data around which the site
is built.

## Inverting Jekyll blog logic

However, we have one slight problem with Jekyll and using posts. Jekyll by
default is for blogging, where posts are expected to be in the past, but for our
calendar all events will be in the future so how do we make jekyll show posts
with a future date?

This isn't such a hurdle as it might seem, Jekyll allows for a configuration
option within `_config.yml` that allows us to publish posts with a future date:

```yml
# publish posts with a future date
future: true
```

I also configure
[jekyll-paginate-v2](https://github.com/sverrirs/jekyll-paginate-v2) to sort
posts for pagination by date. This ensures pagination on the home page with events
listed in upcoming order.

```yml
pagination:
  enabled: true
  per_page: 5
  permalink: "/page:num/"
  sort_field: "date"
```

This is great! It means that my posts model for building the calendar site is a
go-er. It means when building the site Jekyll does actually publish the markdown
posts generated for future dated events an absolute requirement for this site to
work!

To support this the Python script described above also only generates posts
which are dated in the future from the time of execution. Only generating posts
that are in the future ensures the site only pulls through future events because
Jekyll just assumes this is a blog where we've set future
to true.

> One thing I'm actually looking at is how to support upcoming events, as the model described
> here means an event is "popped" out of the calendar when its start time has
> passed. This works fine for events that are short in duration, but for a long
> on-going event (multiple days) it would be better to only "pop" the event from
> the calendar when it has finished (see
> [#67](https://github.com/Sparrow0hawk/rse-calendar/pull/67)).


## Codeless contributions
