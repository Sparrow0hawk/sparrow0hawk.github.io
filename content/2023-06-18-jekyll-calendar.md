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

At this point I'd roughly got myself to where I wanted to be. We had our central
YAML file containing events that we could build a ICalendar file from but we
could also, using GitHub actions + Python + Jinja, create markdown posts to
populate our paginated site home page. We've got an, albeit quite simple,
calendar site that users could browse or subscribe their calendar clients too. 

I configured the GitHub actions to run every day so if there are no pull
requests merged it refreshes the calendar each day, and added some pages
detailing how to add events and a little about page. All I needed were some
contributors! 

## Codeless contributions

I posted in [RSE slack](https://society-rse.org/join-us/) about my project and
had some interest and my first contributor (<3)! Through this process though
they suggested I should have a think about other ways people could contribute an
event, as quite fairly the barrier to entry was quite high (fork repo, edit
locally create a PR). For someone not familiar with git or GitHub this is a real
challenge to getting your event on this site. 

GitHub Pages only hosts static content so you can't use HTTP POST requests to do
any nice form based submissions (to my knowledge). So I needed another way to
enable codeless contributions. My hunch here was that we could probably wire up
a GitHub action to trigger on an issue with a certain label being added. I could
draft a template issue with this label that included some content that mapped to the YAML fields
and pull that out of the issue and append it to my main YAML file and create a
pull request.

Conveniently there already exists an action that will [retrieve YAML or JSON from
code blocks within GitHub
Issues](https://github.com/peter-murray/issue-body-parser-action). This was
ideal, I could draft a template issue with a YAML block that matches the format
of an event in my site YAML file and this action would extract that content. The
more complicated part turned out to be getting this data and appending it to my
existing YAML file.

The
[issue-body-parser-action](https://github.com/peter-murray/issue-body-parser-action)
I used returned the content of the code block as JSON so I now needed a process
that converted that JSON back into YAML and appended it, at the correct level to
my existing YAML file. For this I turned to Javascript, a language I'm less
familiar with than Python but one that has a rather nice library for
manipulating [YAML](https://eemeli.org/yaml/#yaml) with. After a bit of back and
forth with ChatGPT I settled on a rather [rough and ready
script](https://github.com/Sparrow0hawk/rse-calendar/blob/main/_scripts/issue_to_event/index.js)
that did the job, although with no validation. The key thing that really helped
here and why I picked JS was the support in the
[`yaml`](https://eemeli.org/yaml/#yaml) package for YAML features not directly
supported by JS types ([Document API](https://eemeli.org/yaml/#documents)). This
meant I could preserve comments in my original data file that I wanted there for
anyone contributing via a pull request.

Putting this altogether I could now:

- Have a template issue with a YAML code block that matched the right keys for
  adding an event
- Use an existing action to retrieve this YAML block from an issue raised with
  an `add-event` label
- Using the JSON from the above action convert it to YAML and append it to my
  existing calendar data file

The final step was to have the action contribute this amended calendar YAML file
back to the `main` branch as a PR, and preferably include the issue creator as
the contributor.

Again, there already was a GitHub action for that! The fantastic
[create-pull-request](https://github.com/peter-evans/create-pull-request) action
makes it easy to handle committing any changes, making a branch and opening a
pull request with these changes. I can configure the details of who the committer
is so that it uses information about the user who opened the issue, as well as
pull request title and more! This was perfect for what I wanted and completed my
[codeless contributing
action](https://github.com/Sparrow0hawk/rse-calendar/blob/main/.github/workflows/issue_to_pull.yml)
nicely.

## Did you really have to do all that?

I'm reasonably pleased with the [end
result](https://sparrow0hawk.github.io/rse-calendar/) it does what it's billed,
and whilst I'm sure there's probably a better way to do this that doesn't
involve slightly abusing Jekyll's blog logic I worked with what I had.

The codeless contributing bit I find particularly nice as a concept (it's
execution is certainly not perfect and still needs tweaking as seen from peoples
attempts to use it!). The fact you can trigger a whole process that suggests an
automated pull request just from an issue feels like a really nice way to
encourage contributions.

The model I've adopted here for creating a calendar is absolutely transferrable
to other communities who want to centralise their events. All you need to do is
configure the YAML file and update some of the site configuration in
`_config.yml`. So if you have a need to an events calendar and have an audience
that is technically please feel free to check out this tool.

For now, if you're an RSE with an event you want to share please feel free to
[contribute it to the
site](https://sparrow0hawk.github.io/rse-calendar/add-event/). If you're an RSE
on the look out for events check out how to subscribe your calendar client to
the [ICalendar files](https://sparrow0hawk.github.io/rse-calendar/subscribe/).
I'll continue to be tinkering with this for a while so if you've got suggestions
for making it better do [get in touch](https://github.com/Sparrow0hawk/rse-calendar/issues/new)!
