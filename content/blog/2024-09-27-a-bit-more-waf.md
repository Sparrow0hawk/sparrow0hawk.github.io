Title: A bit more on WAFs

In an attempt to more seriously serialize some thoughts lets talk about those
web application firewalls (WAF).  Disclaimer I am __not__ a security person.

A WAF is a firewall for your web application[^1]. You stick it in front of your
web application and apply a set of rules that is uses to allow or deny HTTP
traffic. Rules cover common web application vulnerabilities like cross-site
scripting and SQL injection. OWASP through the ModSecurity WAF project have
come up with some pretty reasonable generic rules called [OWASP
CRS](https://coreruleset.org/) that aim to cover the [OWASP top
10](https://owasp.org/www-project-top-ten/).

WAFs are typically provisioned as a separate infrastructure component that runs
in front of your application. This is an often totted selling point: will you
struggle to test and deploy security fixes? Does a long deployment cycle mean
patches take weeks to hit production? Why not just provision this
infrastructure to cover your back. There’s also a case for a WAF that says when
it comes to application security you should defend in depth.  That is to say
provisioning a WAF is _another_ layer you can wrap around your application in
an attempt to prevent attacks, alongside sanitizing your HTML, content security
policies, enforcing SSL etc.

That all said it ain't all WAFfin' wonderful. WAFs need configuring, you've got
to tell it what rules you want to enforce and how sensitive or
[paranoid](https://coreruleset.org/docs/concepts/paranoia_levels/) you want
your WAF to be.  Paranoid is definitely the feeling this can leave you with,
have I just set a rule that means my users might be a 403 message just for
trying to use my app? This tilts towards the potential issues with a WAF, yes
you can add another layer to your application that will provide protection but
adding another layer means your users have a whole other layer where things
could go wrong.  This also isn't a layer you can replicate locally which means
unpicking any WAF issues becomes a whole lot harder. You can certainly tune the
rules your WAF is enforcing if your users encounter issues but that's one more
thing you've got to work on, one other opinionated bit of infrastructure you've
got to stroke presumably because your application does something that looks
generically fishy.

Which all leads me to wonder how helpful are WAFs? They sure sound nice from a
compliance angle because it's another tickbox, have you got a WAF? Yes, good
job done. But it leaves open fundamental questions, am I as a developer
properly mitigating in the application against attacks like XSS or SQL
injection? Am I picking the right framework that supports doing things in a
modern, secure manner? Am I properly considering the states a user can get into
using my application and if those are secure? I'd be concerned that using a WAF
might feel like a bit of a free-pass that avoids such discussion points. And
whilst advocates of WAFs will, not unreasonably say, a WAF doesn't guarantee
protection there is a danger they don't force developers to actively consider
how to build secure applications and that can't be a good thing.  

[^1]: [OWASP](https://owasp.org/www-community/Web_Application_Firewall) have a
pretty broad definition.

