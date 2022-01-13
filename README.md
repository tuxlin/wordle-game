# wordle game

I'm not sure why I created this but here it is... 

See if you can outperform the computer with a full 5 letter word dictionary and ranking system based on frequency of letter by position in the remaining available words that fit the criteria after each guess. Pass the answer word as a single argument to have the computer guess.

```
$ ./wordle_helper.py words
guess provided: saint
guessing: saint
guess provided: pulse
guessing: pulse
guess provided: combs
guessing: combs
guess provided: words
guessing: words
I win on turn 4

$ ./wordle_helper.py ghost
guess provided: saint
guessing: saint
guess provided: crest
guessing: crest
guess provided: ghost
guessing: ghost
I win on turn 3
``` 

or use the helper function by not passing an answer word and answer provide the results for each letter you entered into Wordle. However, this should be considered cheating and should only be used if you're convinced Wordle is crazy because no word could actually exist with the available letters. :)

green = y
yellow = a
black/white = n (or `enter` as this is the default)

```
$ ./wordle_helper.py

saint
slate
suite
borne
crate
rainy
salty
saner
teary
trine

guess: saint
(S)[y/a/N]: a
(A)[y/a/N]: 
(I)[y/a/N]: 
(N)[y/a/N]: 
(T)[y/a/N]: y

crest
crust
roust
chest
wrest
guest
ghost
worst
burst
frost

guess: crest
(C)[y/a/N]: 
(R)[y/a/N]: 
(E)[y/a/N]: 
(S)[y/a/N]: y
(T)[y/a/N]: y

ghost
joust
boost

guess: ghost
(G)[y/a/N]: y
(H)[y/a/N]: y
(O)[y/a/N]: y
(S)[y/a/N]: y
(T)[y/a/N]: y

ghost

only one word left -- exiting...
```
