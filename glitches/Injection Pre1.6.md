# Injection
One of the main types of glitches in stardew is "injection". This is  preformed by putting what can be thought of as code in a name textbox, that is then read through a dialogue box and the game processes it as code. This is commonly done in the player name, farm name, favourite thing and animal names. There are a few types of injection: item injection, mail injection, flag injection and cutscene injection.

## Item Injection

### Overview:
Item injection is when you have an NPC or more generally, the correct type of dialogue box say text containing the item ID for an item, and this is how the game handles giving the player items inside dialogue(eg willy giving a pearl if you have a fishpond with 10 crabs in), and we are just abusing this. This page is all assuming simplified chinese as the language as it has the smallest font. If it is not this type of dialogue box this does not work.

### Basic example:
`[434][0434][00434]`

Putting this as the player name and then having the player name said in the dialgue would give 3 `[434]` items, which happens to be a stardrop. The version for up to 1.5 prepends with `0` and `00` respectively since in those versions all item IDs are numeric, and the game will not inject duplicate item IDs. The alterative way to distinguish an item ID is prepending with a combination of new line characters, tab characters, vertical tab characters and plus(+) signs so it could look like the below example and the game when converting it into a number, will interpret it as `[434]` still, but not recognise it as a duplicate. In 1.6 item IDs are unique and handled as strings, and dont have this non duplicate issues. The smallest character for creating non duplicates is the tab character.
```
[+
434]
```
### Item Limits:
Different dialogue boxes can also inject a different maximum number of items dependant on how many text boxes there are. Specifically if it is the last dialogue box of the dialogue chain, e.g the robin dialogue on the farm in the intro cutscene, you can get 3 items, and otherwise only 2, for example robin saying the farmer name outside the bus in the intro cutscene, since there are more text boxes after the one with the name said.

### Item Limit Extension:
In some situations the item limits per dialogue box are too small, there are a few methods to get around this. If you are on versions 1.3 or earlier there is [WSC](Window%Shift%Cancel.md), artificially adding additional text boxes to the dialogue(by extending the name), or in the case of animals sold by marnie, you can increase the maxiumum quantity of items injected from 3 to 6 by inserting a `#` after the first 3 items which are processed, this is the internal character used by the game to split off dialogue boxes. Note that this this is processed before substituions talked about below, so for example you can name a chicken `%favorite#[350]` with the player favourite thing being `[597][188][190]`, then the game will give all 4 items, however if it was `%favorite[350]` with favourite thing `[597][20]#[190]` the game would not process the `#` and you would only get 3 items.

You can also make the players name very long, causing there to be more text boxes working to process the same name. This is done optimally by doing something along the lines of `^^^^^^1^^^^^^2^^^^^^3`, as the `^`'s are read as newline characters. (This does require having an intentional gender switch block to avoid the `^`'s getting read as gender switches, but that can be easily handled by starting with a `¦` and playing as a female)

### Substitutions:
Sometimes(for example in NDE aka no dialogue extension catagories) we are limited by space in the text boxes we have available, or otherwise wish to not directly have the paste in the player name. Luckily the game has a few useful shorthands for dialogue writing which we can abuse to increase our effective space, which are processed in a specific order.

- `@` - replaced with player name
- `%farm` - replaced with farm name
- `%favorite` - replaced with the players favourite thing
- `%kid1` - replaced with the name of the 1st child
- `%kid2` - replaced with the name of the 2nd child
- `%pet` - replaced with the name of the 1st pet on the farm

Note there are other replacements, but no other player inputtable ones, and realistically `%kid1` and `%kid2` are not practical to use in any speed context.

## Flag Injection
### Overview:

A lot of variables are secretly controlled by “invisible” pieces of mail (such as being able to read junimo text), and these invisible pieces are called Flags. In versions 1.0-1.5, whenever the game seeds a } in dialogue, it thinks all text before it is a flag it should send to the player. We can abuse this by including `FLAG}` in our name.

Notably, however, it does *all* text previously. As such, if we want it to be a simple string and not an entire sentence, we need to make it so that our FLAG are the first characters in the text box.

There are two main ways to do this. The historical way has been to name the player `}FLAG}`, as this causes the game to see the first } as a flag, send that, and then on a second pass notice our FLAG. 

The second (and better) way is to name ourselves `¦FLAG}` while playing as a girl. The `¦` (or `^`, but that's wider) is read as a gender switch to consider all dialogue to the left of it male-exclusive, causing all text to the left of it being deleted without using up a flag-pass.

The reason we are concerned about the extra `}` is because, just as for [ID], the game will only process 2-3 flag injections per text box. By using a gender switch rather than a `}`, we can inject an extra flag.

(It also means that if you're using [WSC](Window%Shift%Cancel.md) there's no point to using `¦` - as you aren't subject to the injection per box limit)

### Useful flag names and how to implement longer flags:

- list of useful flags and where more can be found(modding wiki) 
