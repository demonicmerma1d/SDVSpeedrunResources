# Pastes
The NDE pastes are [here](/routes/Pastes/NDEJojaMovie260424.txt), and the glitched pastes are [here](/routes/Pastes/GlitchedJojaMovie260424Copypasta.txt)
Note the only difference between the pastes is that the glitched one deliberately uses dialogue extension to legally not be an NDE run, via starting with a copypasta.

# Route

### Important details
- Run on version 1.5(.6), below 1.5 the crash handling ` ][` we abuse in the name does not exist in prior versions and the game hard crashes instead of exiting the cutscene, and flag injection does not work in this way on version 1.6.
- In chinese, for normal glitches reasons(small font), this is more relevent for NDE however these pastes are designed with chinese font size in mind.
- Female character: we are abusing dialogue gender swapping characters to enable a second flag inject on 1 dialogue box.

### The Run
1) Setup the file.
2) Skip through intro(press Esc 2x)
3) Time ends when the cutscene crashes, this is best timed using a day 0 end autosplit
4) Verify that the movie theater exists(this is what the magic rock candy is for)

### Paste explaination
Since the only difference between the NDE and glitched pastes is for technicalities, we will be focusing on the NDE paste.


The Dialogue string:
`blah @ blah`
1) The game substitutes the player name into the string.
`blah¦%favorite}%farm ][ blah` 
2) The game substitutes the farm name `%favoriteJoja}[279]` into `%farm`.
`blah¦%favorite}%favoriteJoja}[279] ][ blah`
3) The game substitutes the favourite thing `ccMovieTheater` into `%favorite`
`blah ¦ccMovieTheater}ccMovieTheaterJoja}[279] ][ blah`
4) Being female -> Game deletes all previous text in the dialogue box due to the gender switch statement `¦`
`ccMovieTheater}ccMovieTheaterJoja}[279] ][ blah`
5) The game parses `ccMovieTheater` as a mail flag.
`ccMovieTheaterJoja}[279] ][ blah`
6) The game parses `[279]` as an item to inject
`ccMovieTheaterJoja} ][ blah`
7) The game parses `ccMovieTheaterJoja` as a mail flag.
` ][ blah`
8) The game attempts to parse ` ][` to look for items to inject, bypasses the check for starting a string with `]` due to the space, resulting in getting a substring of length -1, triggering crash handling.



