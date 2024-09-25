Title: What the WAF

So you've written a web application and you want to stick it on the world wide web. 
You've tried you're best around security, your app's containerised, running on some container runtime service, 
secrets are managed using a secret manager, your escaping all user input before it goes into any server-side rendering 
and using an ORM to compose all your SQL queries. Your users have to authenticate using a [modern authentication protocol](https://openid.net/developers/how-connect-works/)
and managing a discrete user allow list. 
Maybe you've also plonked a load balancer in front of your cloud container service, just in case ya know you don't want to be DDoS'ed.
Only your devs have write access to the repo and you've got some static code analysis tools to check for vulnerabilities in the source code and dependencies.

I could go on, you've tried your best, tried to be sensible, followed the advice, you've read [OWASP top 10](https://owasp.org/Top10/). 

You get it, security it's important, it's not easy.

A paper missive lands from on high, where's your [WAF](https://en.wikipedia.org/wiki/Web_application_firewall)?

Where is it? Well alongside wrapping your head around the business logic, how to test and deploy, setting up your infrastructure, 
installing your favourite IDE, working out what stack to pick, sorting out a WAF got missed off.

So you go off and read about your WAF because your paper missive has no instructions. Just a WAF now please it says.
And what you find is it's bloody complex, you've got to pick some rules, you've got to pick some [paranoia levels](https://coreruleset.org/20211028/working-with-paranoia-levels/) 
because the WAF might actually block legitimate use cases. Waffy faffy more like.

At this stage you learn to stop worrying and love the WAF or more accurately love the [Core Rule Set](https://coreruleset.org/).

Here endeth the lesson.