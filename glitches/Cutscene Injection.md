# Cutscene Injection

## Version Limits
Cutscene injection works on versions 1.0 through to 1.5, 1.6 added sufficient input sanitisation so you can no longer brick your game and be forced to Alt F4 if you had an specifically formatted name, and then died. (The name format for this would be similar to `/text `). This would cause the game to get stuck mid cutscene since it attempts to read whatever is after the `/` as a cutscene command but there is no non whitespace character at the end to signalling the game to terminate the command.(note: fact check this)

## Mechanism
Similar to other injection glitches, cutscene injection operates by inserting valid command inputs into the player name, which when the game replaces the player name into a event(cutscene) script inside a dialogue, it proceeds to attempt to execute the injected commands. The events which are useful for this are both the mines and hospital death events.

### Deadly Friendship
Notably in almost all circumstances this requires [dialogue extension](/glitches/Dialogue%20Extension.md). The main practical exception to this is from the old 1.2 NDE marriage route for Alex/Maru, with a strategy called "deadly friendship", a concept developed in 2017 by BlueCheetah. 

Deadly friendship involves naming the player `/friendship Alex 99 .` and `/friendship Maru 99 .` respectively for Alex and Maru(no other marriagable npcs have short enough names to fit within the line limit), then chain dying in the mines to repeatedly trigger the mines death cutscene, which says the player name.

### Dialogue Extension
In order to maintain valid syntax over newlines, you have to smuggle the newlines either inside the `speak` command, which is how dialogue is implemented in events, or as the whitespace character between command arguments, since this gets parsed out on execution. Both of these can be seen for example in the below paste, which is the paste for (1.2) glitched Harvey marriage.(credit pending)

player name:
```
%farm
/speak Harvey "
[460]"
/friendship Harvey 
9999
/addTool Wand 
/skippable 
/end position 10 2 .
```
Farm name:
```
[460]
[288][0288][00288]
[000288][0000288]
```

## Key Commands and Elements
Note: These are predominantly paraphrased or directly copied from [here](https://stardewvalleywiki.com/mediawiki/index.php?title=Modding:Event_data&oldid=153365).
- `/` - This is the delimiter character between commands.
- `speak <character> "<text>"` - This makes an NPC speak, either to execute item injection and/or flag injection, both described [here](/glitches/Injection%20Pre1.6.md). Also makes the player meet the given NPC.
- `Friendship <name> <number>` - This attempts to add a given friendship amount `<number>` to `<name>` if they are in the friendshipData, which requires the npc to be met by the player.
- `end` - This is the generic event ending command, with multiple previously useful variants in speedrun routes.
    - `end warpOut` - Ends the cutscene and places the player at the first warp out of the current location if female, else at the second one if male and in the bathhouse.
    - `end position <x> <y>` - Ends the cutscene and places the player at the coordinates (x,y) in the current map.
    - `end newDay` - Ends the cutscene and ends the day.
- `addTool <Sword|Wand>` - Adds either an unimplented sword("Battered Sword") or the Return Scepter(useful, this is `addTool Wand `, since this is the only way to give the player the Return Scepter prior to 1.6).
- `catQuestion` - Triggers the Marnie pet naming prompt, useful for setting the `%pet` variable while in the death cutscene. For example this is used in the 1.2 glitched CC route.
- `skippable` - Lets you skip the remaining portion of the event.
- `playerControl` - Gives control back to the player and lets you walk around within the cutscene. Note: this is not helpful ever but its funny to do once.