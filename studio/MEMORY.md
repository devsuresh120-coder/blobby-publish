Blobby & Co. — shared memory (source of truth across threads)

Claude updates this file. Do not edit by hand except BC_PUBLISH_NEXT_DAY on launch.

BC_LAST_EPISODE: 42

BC_OPEN_BATCHES:

BC_DONE_BATCHES:

1-2 reference 2026-10-16
3-12 batch-mixed 2026-10-16
13-22 batch-mixed-2 2026-10-16
23-32 batch-creative 2026-10-16
33-42 fast-hook-loop 2026-10-20
BC_PUBLISH_NEXT_DAY: 2026-11-07

BC_USED_JOKES:

1 | monday-alarm | 5am alarm productive flex faceplant bed asleep motivation 3 seconds
2 | what-do-you-want-to-eat | partner anything is fine pizza burger noodles rejected nothing is fine
3 | umbrella | sunny day leave umbrella home door locks rain soaked forecast
4 | cold-feet | bed night partner icy feet back shiver eyes pop jump ceiling
5 | diet-day | diet salad morning fridge midnight stare pizza cheat day one
6 | four-fifty-nine | office clock 4:59 pack bag boss arrives paper new task stay late
7 | where-is-my-phone | search room sofa panic partner points phone in hand
8 | ignored-until-food | cat ignores calling sleeps fridge opens cat instantly appears
9 | one-more-episode | tv just one episode remote clock 11pm 3am sunrise binge
10 | im-fine | partner says fine arms crossed anger flames sweat apology
11 | thumbs-up | long report weeks work send boss reply k one letter sad trombone
12 | which-sleeper | poll sleeping positions starfish burrito falls off bed phone scroll 3am
13 | gym-day-one | gym first day flex tiny dumbbell lift collapse floor day 1 of 1
14 | phone-1-percent | battery 1 percent panic run charger across room dies at plug
15 | delivery-box | doorbell parcel happy dance giant box tiny item inside
16 | coffee-count | poll coffee cups one three whole pot jitter which are you
17 | i-dont-want-any | partner says no thanks orders nothing then eats all his slices empty plate
18 | five-more-minutes | partner ready at door wait five minutes clock forty later still getting dressed
19 | shopping-bags | partner shopping trip he carries all bags squashed she carries only phone
20 | reply-all | email complaint accidentally sent to everyone ding ding boss appears hide
21 | raise-request | ask boss for raise confident stare shrinks tiny leaves
22 | cup-off-table | cat eye contact paw pushes cup off counter crash frozen owner
23 | doorway-amnesia | walk into kitchen determined forget why question walk back remember forget again doorway
24 | bluetooth-not-connected | headphones dance street music phone speaker everyone heard bluetooth off
25 | essay-then-ok | angry long message typing rewrite delete send haha ok bed night
26 | party-type-poll | poll party types dancer snack table pets cat leaves early
27 | already-watched-ahead | couple series together secretly watched ahead poker face yawn spoiler caught
28 | notice-anything-new | partner asks notice anything new haircut 1 cm guessing panic
29 | identical-choice | partner holds two identical options which one pick wrong same colour
30 | not-muted | video call thinks muted sings dances boss stares unmuted mic
31 | waved-back-wrong | stranger waves wave back enthusiastic waving at person behind fake stretch
32 | midnight-ball-trap | cat ball floor night tiptoe water step silent scream cat grin
33 | cooking-video | recipe video kitchen fire explosion order pizza delivery
34 | blanket-war | 2am blanket pull partner wins floor
35 | quick-call | boss 5 minute call lasts all day 8 hours
36 | saving-money | no spend month sale notification box next day
37 | 5am-cat-alarm | cat wakes owner 5am sits on head no snooze
38 | photo-of-me | take a photo 87 photos all wrong partner angry
39 | public-wifi | free wifi loading phone in the air zero bars
40 | boss-good-job | boss praise reward more paper work pile
41 | gift-socks | big gift box socks fake smile
42 | weekend-type | poll sofa gym party sleep A B C D
BC_FORMAT (since ep 33, hard rules):

12-13 s, seamless loop (last beat = "Next day:" bridge back to beat 1), loop=True, voice=False
no end card, no on-screen question, no voice line; the question goes only in description / pinned comment
frame one = action + sound, first caption 1-3 words, punchline by ~8 s
max 2 short non-verbal human reaction sounds (vox) per video, never words
TikTok is manual (no TikTok rows in Buffer); each batch also gives a tiktok_manual zip
reference batch: code/ep33_42.py in blobby_pack.zip