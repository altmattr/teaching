https://youtu.be/RDJmhHhnZYQ?si=tba7lbSIHUpeRbwM

0:00
Okay, good day all. We're going to going to chat
0:02
about the week four problem and just
0:05
point at some possible paths or
0:08
solutions
0:10
uh to this task. So, it's not a very
0:12
well defined task and that's where a lot
0:14
of the tasks go in com 3000.
0:19
So,
0:21
we're really starting to look at our
0:22
overall goal, which is to create a
0:24
language for modeling river flows and
0:27
starting to think about what that even
0:29
means. Uh, simulating is maybe a better
0:31
word than modeling, or a more familiar
0:34
word than modeling. You wanting to take
0:36
the characteristics of a river system
0:40
and simulate what's going to occur in
0:42
that river system based on certain
0:44
rains. So if I just make a pretend river
0:47
system,
0:50
it's got two rivers coming into there
0:52
and another river coming into there and
0:53
another river coming into there. And
0:55
then so if that's my pretend river
0:58
system, it's got multiple parts. It's
1:01
got this branch called A, this branch
1:03
called B, this branch called C, and then
1:06
there's this main river here as well.
1:11
to to to understand this or to to to
1:13
model it, I need to chunk it in some
1:16
way. And that's part of the design
1:19
decision about how you're going to
1:21
define a um a river system as a
1:24
programming language uh or as a as a
1:27
program in a programming language.
1:29
That's really what we're trying to do
1:30
here. Like I could say this river system
1:32
is um a data structure that holds an A
1:35
and a B and a C and does certain things,
1:37
but I don't want it to define it as a
1:39
data structure. I wanted to define it as
1:40
a program in a programming language.
1:42
That's the conceptual jump we're trying
1:44
to make here.
1:46
Okay.
1:49
So, the first thing is to chunk it. And
1:51
I tried to show you uh an example way to
1:53
chunk it. Uh which I'll do here again.
1:55
And the way I chunk it is I just find
1:57
all the the connection points and I say
2:00
something's happening at that connection
2:02
point. So, I care about what's happening
2:04
above that connection point.
2:13
And I care what's happening within that
2:15
connection point.
2:17
If I think about it in terms of rain
2:19
falling down, I know that when rain
2:23
falls in this region, it flows down
2:26
creek B. And when it falls in this
2:28
region, it'll flow down creek A. And
2:32
when it falls in this region, it's going
2:34
to be added into the flow for that
2:36
creek.
2:38
Falls in this region, flow for that
2:40
creek. Falls in this region, it's added
2:43
into the flow for that creek. So, it's
2:46
not a bad way to break it up. And that's
2:48
what I've pointed towards here. And each
2:50
of these I'm going to call maybe a
2:52
catchment or a watershed. Those words
2:54
are fine. Or a creek system.
2:57
But I've got one, two, three. I've
2:59
actually got a fourth and a fifth here.
3:03
A, B, C, D, and E.
3:06
So, rainfall equals water in river.
3:10
That's a good start.
3:16
Leads to let's say leads to because
3:18
we're going to avoid using equalities
3:19
because they mean something in a
3:20
programming language.
3:30
Okay, so the rainfall the the amount of
3:33
water flowing down creek A is going to
3:35
depend on the amount of rainfall that
3:37
happens. But let's just assume I've got
3:39
a certain amount of rainfall X.
3:43
So if I look at if I look at creek A or
3:46
catchment A, it's relatively small. So
3:48
if there was x rainfall, there might be
3:51
say 2x
3:54
water flowing down that creek. And B is
3:57
probably the same. It's probably 2x
3:59
water flowing down that creek.
4:02
Now D, you the area for D is bigger. So
4:06
there's probably 3x water falling in
4:08
that area.
4:10
C,
4:12
it's probably small as well. Let's make
4:14
this one a bit even bigger. Let's make
4:16
that 4x.
4:19
Then this one would probably be 3x. And
4:21
this one here is probably another 3x. So
4:24
each of these catchments now has a size
4:27
indicating how much water gets captured
4:30
every time there's some rainfall
4:34
overall. Then I might say that the total
4:37
rainfall from this system
4:40
is
4:42
2x
4:44
plus 2x. So that's
4:47
a and b
4:53
plus 4x
4:56
+ 3x + 3x, right? And that's
5:02
a, b, d, c, and e all flowing into that
5:07
river system.
5:09
So just by exploring this idea, I've
5:12
gotten to a an expression here
5:17
that represents
5:19
how much water is in the river.
5:23
Coming out of this point here, coming
5:25
out of point here on the river.
5:29
Cool. This is me starting to model a
5:31
river system. What I want you to notice
5:32
at this point is hey if I were to choose
5:34
to model my river system this way. This
5:37
was my decision. I need then this text
5:40
here is going to get written in my
5:42
program somewhere.
5:45
And then if that text is being written
5:47
in my program my scanner needs to
5:49
support that text.
5:52
Yeah.
5:53
So we ask ourselves uh so we would need
5:56
a SK because scanners are what we're
5:58
doing at the moment.
6:06
Now as it turns out the scanner that
6:09
we've got won't support this.
6:12
Uh the scanner that we've done so far in
6:15
the course can scan numbers. Well, let's
6:18
go let's go double check on it.
6:26
crafting interpreters.
6:30
Jumping over to the scanner.
6:34
Okay, so we've read this already, so we
6:36
can scroll through it quickly. And I'm
6:37
just looking to see all the different
6:38
things it's going to scan. So I remember
6:41
it had these token types to help me out.
6:43
So these are the different things it can
6:45
scan. Okay, it can definitely scan the
6:47
plus that I put in there.
6:49
It can definitely scan the numbers that
6:51
I put in there. And it can also scan
6:53
that X. It scans it as an identifier.
6:55
So, let's scroll down a little further
6:56
to see how it scans that identifier just
7:00
to convince ourselves it's going to do
7:01
an X. Here's how it scans the plus. And
7:04
that's just fine. What we expected.
7:07
Um,
7:10
more operators, longer lexims.
7:14
We're peeking ahead.
7:16
String literal. That's not what we've
7:17
got here. number literal. So definitely
7:19
scans a number literal. In fact, I could
7:20
put 2.1x and my current scanner would
7:23
still deal with it.
7:26
And do we do identifiers? Yes, we do. So
7:28
then what happens is in this particular
7:30
scanner, if it's not anything else, we
7:33
just scan it as an identifier and double
7:35
check it against our keyword. So our
7:36
scanner will happily scan this string
7:39
that I put in there. So, if I just got
7:41
the standard locks interpreter, this
7:44
would be scanned into I'm just going to
7:46
do a few of them, but a number,
7:50
which is the two, an identifier,
7:58
which is the X,
8:00
then a plus, and so on and so forth. So,
8:04
yeah, the scanner is going to be just
8:05
fine for this. I've got a representation
8:08
of a river system. I'm interpreting this
8:10
string 2x plus 2x plus 4x plus 3x in a
8:13
certain way. My scanner can cope with
8:15
that just fine. So maybe there's nothing
8:18
to do. Maybe I'm already on my way.
8:20
Well, even if you've just done this,
8:22
you've done a big step this week because
8:24
you've started to think about uh river
8:27
system in terms of a program written in
8:29
a custom programming language. So good
8:31
job done.
8:34
But let's step it up one more. Let's say
8:35
I wanted to make this a slightly more
8:37
sophisticated system. Let's say I wanted
8:41
to, as I intimated in the questions
8:43
here, say that the water when the rain
8:45
falls, it doesn't immediately appear in
8:47
the river system. I'll redraw my river
8:50
system so I can scribble on it again.
8:56
Let's say that when rain falls, we we
8:59
had river system A, B, D, C, and D. I'm
9:04
still breaking it up in the same way. I
9:06
won't put the orange parts on there just
9:08
to make it easier to read this.
9:11
What if I wanted to say that when x
9:13
amount of rain falls
9:17
on day one,
9:20
one x gets into the the river. And on
9:24
day two,
9:26
one x gets into the river. Sorry.
9:31
And on day three, we're done. 0x gets
9:34
in. 0x gets in. So all the water flows
9:37
in over two days. Half of it in the
9:39
first day, half of it in the second day.
9:42
But river system A is much steeper. So
9:45
on river system A, 2X goes in on the
9:48
first day. No X goes in any other day.
9:52
Yeah. River system D maybe is super
9:55
shallow. So maybe river system D, the
9:57
rain comes in at 0.5x
10:00
0.5x
10:03
0.5x
10:04
0.5x. That gets me my uh river system D
10:09
was four. So in fact, let's make it
10:12
shallow, but it still gets quite a lot
10:14
coming in because it's a big system,
10:16
right? So it'll get 1 x, 1 x, 1 x, and 1
10:21
x, and then zero x on forever.
10:25
C got three. Let's make that one shallow
10:28
as well. So it can go 0.5x
10:30
0.5x
10:32
0.5x
10:34
then 0x forever.
10:38
And finally E will do a faster version.
10:42
Oh sorry that was wrong. That was again
10:45
that was not enough because river system
10:48
C gets three in total. So 1 x 1 x 1 x 0x
10:57
and let's make e go 1 x
11:00
1 x and then start to slow down
11:05
and then 0x.
11:08
So what I'm doing here is I'm just
11:09
upping the ante a little on what I'm
11:11
modeling.
11:14
And if I follow the path that I did
11:15
before, I'm going to end up with a
11:17
fairly complicated thing. So I won't
11:19
write the whole thing out.
11:22
But the flow in the whole river is
11:23
somehow the addition of this
11:30
the thing I suggested for a which was 2x
11:34
nx onwards forever
11:38
plus whatever's happening in b which I
11:40
said was 1 x 1 x
11:44
0x going on forever
11:47
plus whatever's happening in D which I
11:49
said was 1 x 1 x
11:53
1 x
11:55
1 x and then 0 x going on forever
11:59
plus uh that will continue right so now
12:03
I've got a more complicated
12:06
string for my program and I don't know
12:09
anything about how this program gets
12:11
evaluated or anything I'm only thinking
12:14
what strings might I need to express
12:17
what I'm trying to capture
12:20
Um, and here I see my scanner. Oh, does
12:23
my scanner cut it? Let's find out.
12:27
If I scroll back up to my token types,
12:29
are there any token types I've used in
12:31
that that don't exist?
12:34
Turns out not. All the tokens that I
12:36
need are here. So, I've still got
12:40
everything I need to scan it, but it's
12:42
going to scan into a different form.
12:45
Okay, cool. So again, no changes needed
12:47
to the scanner, just changes needed to
12:49
my thought processes and understanding.
12:50
Oh, actually, no, that's not true.
12:54
Specifically,
12:55
those dot dot dots I put in, I put them
12:57
in just for convenience, but I've
12:59
decided they mean something. I've
13:00
decided, you know, um I'm modeling this
13:03
river system and I'm saying, you know,
13:05
here's here's when the water starts to
13:07
fall, starts to get into the creek, but
13:09
once you get to a 0x dot dot dot,
13:13
that means no more water's coming. I can
13:15
just stop in my in my little this string
13:17
that I just made up. Totally made this
13:19
up. You'll have made up your own.
13:21
So the dot dot dot is not being scanned
13:25
as a single token in my language, is it?
13:30
The dot dot dot is being scanned in this
13:32
language as a dot
13:36
dot at a dot. There's a dot scanner, but
13:38
it just scans one dot at a time.
13:42
All right, that might be okay. it might
13:44
not be okay. We won't discover until we
13:46
get to the pausing phase. But at this
13:48
point, we notice it and think about it.
13:53
Okay, so these are very abstract
13:56
questions, right? Where we're just
13:57
trying to guide you into thinking about
14:00
the things that are going to be needed
14:01
further down the track. This is the big
14:03
challenge with doing something as
14:05
interesting as this. It's that the
14:08
amount of thinking required
14:11
up front to get into the task that
14:13
you're trying to do is significant. So
14:15
in your teams and through the tasks
14:18
we're giving you, we're trying to prompt
14:19
you into that thinking. I'll give you
14:22
one more change just so that I end up
14:24
with a language that does need something
14:25
in the scanner.
14:27
In the end, I decided uh I didn't want
14:30
this dot dot dot. I just wanted to
14:32
assume that after 3 days,
14:35
all the water's done.
14:37
So my language started to look like a it
14:40
went 2x or sorry
14:45
2x
14:48
nx x right plus and then the next one
14:50
was 1 x 1x nx so exactly three every
14:55
time
14:57
that was a just arbitrary decision I
14:59
made the trouble now well then I think
15:02
to myself h have I chosen a good syntax
15:04
for these things if there's always
15:06
exactly three of them. These feel a lot
15:08
like arrays or something to me. I think
15:10
it would be more meaningful to me as a
15:12
programmer if I made those square
15:16
brackets. Probably even on the other one
15:18
back here. I probably even wanted square
15:20
brackets back here now that I'm thinking
15:22
about my problem.
15:24
And now I hit a point where my scanner
15:28
isn't
15:30
doing that for me. There's nothing in
15:33
locks itself that uses square brackets
15:35
that we've seen. So there's nothing in
15:37
the existing lock scanner. So I would
15:39
have to extend my scanner at this point
15:41
if I decided the best syntax for me was
15:43
square brackets. And what I want you to
15:46
know is that the right syntax matters.
15:52
So do think about sensible syntax
15:56
even if you have to change your paraser.
16:00
That little diamond there means change.
16:02
Uh, sorry, not your pass, your scanner.
16:03
We will change the PA next week, even if
16:06
you have to change your scanner.
16:11
So, in my case, I might then go through
16:12
and think to myself, well, what changes
16:13
do I have to make to my scanner? That's
16:15
what we encourage you to do. Maybe even
16:16
make those changes so that your locks
16:18
interpreter uh or your lock scanner,
16:21
which is what you got at the moment, can
16:22
run. I'll quickly cover those here. I
16:25
would need a new token type because I
16:26
don't have one for this yet. So I would
16:29
put a token type maybe left square and
16:32
right square.
16:35
That would do uh to go along with the
16:37
left parentheses and the left brace.
16:40
Then down here I would have to make a
16:43
change to the actual scanner class, just
16:45
the one where it looks at an individual
16:46
token. And if it sees the square
16:48
bracket, I got to add the token left
16:50
square and right square and break.
16:51
That's probably all I got to do. Uh, I
16:54
should do that though and put those
16:55
changes in and try them out before I'm
16:57
convinced that's everything I have to
16:58
do. But I'm pretty sure that's it. Once
17:01
I'd done that, I would then be able to
17:03
put these things here
17:06
into
17:09
a text file and run my lock scanner over
17:11
it and see what lock spits out. So, I
17:14
would have created a tool that can help
17:15
me manipulate those things. That's
17:17
exactly where we're heading. So, the the
17:20
best teams will have made it to that
17:21
point by the end. They will have made a
17:22
decision. they will have made some
17:23
change to their scanner and they will
17:25
put some example programs into a text
17:28
file and run their scanner over them to
17:30
be prepped for next week where surprise
17:32
surprise we start to think about pausing
17:35
uh for these these terms. Now I want to
17:38
make very clear I said it at the start
17:40
but I'll say it again at the end. The
17:41
reason I've written week four ideas here
17:43
not week four solutions is these are not
17:46
either the right solutions or the best
17:48
solutions or the solutions you should
17:50
follow. This is me exploring one of the
17:53
solutions so that everybody can catch up
17:58
to the the the level of thinking that's
18:01
required to make the next step. Your
18:04
team will have had a different syntax
18:06
and it's probably better to stick with
18:07
that syntax because the syntax is
18:10
matching what you're talking about
18:12
together and what you're internalizing.
18:14
If you jump ship and go, "No, no, now
18:16
we're all going to internalize Matt's
18:17
version that he happened to do in his
18:19
answer," you're really just making life
18:20
harder for yourself.
18:23
Okay. But I do recognize that some teams
18:26
won't have gotten to an answer. Some
18:28
people won't really know where this was
18:30
going. So that's why we've done a video
18:32
just to help explain one of the paths.
18:35
All right. See you nex
