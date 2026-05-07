# 1.6 Injection
## Notes
This is a supplementary page to the [pre 1.6 injection](/glitches/Injection%20Pre1.6.md), for an overview of the concept of injection glitches in stardew, go there. This page is to detail cases where the game behaves differently in 1.6 versions.

## Item Injection
### Injection Differences:
In version 1.6, when the game interprets a dialogue string with item ids in, for example `[128][128][132][132]`, it will give you all copies of an ID, and has no limits to how many items can be injected per textbox. It also processes all the items to inject instantly, instead of doing it one by one. 
Internally item IDs are also qualified strings, for example an item from `Objects.json` (in previous versions this was `ObjectInformation.json`), would be interpreted by the game and qualified with an `(O)`, for example `[(O)251]`. A side effect of all item IDs being qualified instead of the game only looking for items from `ObjectInformation.json` directly is that we can now spawn in more types of item. The types in the game are:
| Type                 	| Qualifier      	| Data Asset(for item IDs)           	|
|----------------------	|----------------	|------------------------------------	|
| Objects              	| `(O)`          	| `Data/Objects`                     	|
| Big Craftable        	| `(BC)`         	| `Data/BigCraftables`               	|
| Furniture            	| `(F)`          	| `Data/Furniture`                   	|
| Weapons              	| `(W)`          	| `Data/Weapons`                     	|
| Boots                	| `(B)`          	| `Data/Boots`                       	|
| Hats                 	| `(H)`          	| `Data/Hats`                        	|
| Mannequins           	| `(M)`          	| `Data/Mannequins`                  	|
| Pants                	| `(P)`          	| `Data/Pants`                       	|
| Shirts               	| `(S)`          	| `Data/Shirts`                      	|
| Tools                	| `(T)`          	| `Data/Tools`                       	|
| Trinkets             	| `(TR)`         	| `Data/Trinkets`                    	|
| Wallpaper & Flooring 	| `(WP)` & `(FL)` 	| `Data/AdditionalWallpaperFlooring` 	|


When you give the game an unqualified item ID, it searches for the first instance of that id from each type in the order they are in the table above. 
Useful Items this enables you to spawn in that were previously impossible include things like `[(T)ReturnScepter]` for the Return Scepter, instead of using the [cutscene injection](/glitches/Cutscene%20Injection.md) for it (this is convinient considering that cutscene injection is no longer possible). However due to other code changes, something that was useful to inject occassionally in 1.0 - 1.5, the Dwarvish Translation Guide `[326]`, which when injected would vanish and give you the ability to talk to the dwarf, no longer works and it is just an item you can pick up and place down. The other resulting change of using string IDs is that something of the form `[128][0128]` would spawn one pufferfish (`[(O)128]`), and then fail to find an item with the ID `[0128]` in any of the data files, since that worked based on the 1.5 integer id parsing.

### Substitutions:
Underlying in the code some substitutions were moved to a different point in the process, for example `%adj` which generates a random adjective, however all of the functional ones still work.

## Flag Injection
### Flag Injection Differences:
Due to where mail flags are now processed inside dialogue, the only way to inject a mail flag is in an animal name at Marnie's. This is by doing something either of the form `#FLAG}`, which works regardless of gender, and you can prepend with other injections, or with the female gender you can do `¦FLAG}`. This has a limit of 1 flag per dialogue.

### Non Flag uses:
Due to other changes in dialogue code (specifically the fact there is now a second check for voiding and not showing a textbox if it is blank), if you name an animal something of the form `}[128][74][16]#`, the game will parse out all the dialogue it would play, execute it but also skip the dialogue box since there is nothing remaining to show, which is a small timesave. This can be done more space efficiently with the male gender, with the format `}[128][74][16]¦`.
This also works when the player name is said on a telephone call, and works alongside substitution.

## Playing Cutscenes
### Mechanic:
As of 1.6, animal names at marnie can also be co-opted to play vanilla cutscenes(events), signalled by `$v`, eg `[16]#$v 112 false ` which would give a horseradish and play the cutscene where you unlock the ability to see the community centre bundles. The `false` indicates to not check if you meet the conditions to play the cutscene, and an additional false, eg `#$v 112 false false ` would indicate to not check for if it has already been seen. The trailing whitespace is important for parsing so it runs. At the end of the cutscene you are placed on the map where the cutscene is, at the default warp coordinates for the map. 

### Cutscene Wrong Warp:
Using this injection, you can also attempt to play things which are internally events but are forking branches of other events which are normally only triggered as part of other events depending on player dialogue options (for example "Punch", which is the punching Morris option when you watch the community center complete cutscene). This causes the game to throw an error when initialising the cutscene, auto ending it as it would start, placing you in the location it would take place in. However, since it failed to initialise the event, the game never updated the end coordinates, so you are placed at whatever coordinates were stored as the end position from the last cutscene you watched, typically somewhere out of bounds/in a wall.

## Action Injection:
See [mail injection](/glitches/Mail%20Injection.md), since it is functionally equivelent, but different syntax.