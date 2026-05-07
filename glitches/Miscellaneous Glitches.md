# Weapon Out Of Bounds:
## Notes
- Works on all versions.
## Mechanic
Swinging a weapon pushes you in that direction slightly (more significant if you animation cancel to prevent the backwards momentum in the latter half of the animation). This advances you through loadzones without triggering you going the transition. You can then safely walk around out of bounds.

# Bouquet Friendship
## Notes
- Works in versions 1.0 - 1.3.

## Mechanic
The game does not recognise Bouquet as a gift, but it gives 25 friendship, so you can repeatedly give them to a marriageable NPC with at least 8 hearts of friendship to keep gaining friendship. It takes 20 to get to 10 hearts.

# Save Skipping
## Notes
- Works in versions 1.0 - 1.3.
- For more extensive 1.2 glitched routes this is strictly required, at least on Windows due to utilising [cutscene injection](/glitches/Cutscene%20Injection.md), resulting in a long player name, and since prior to 1.5 save files saved with the farmer name instead of the farm name, this results in a really long file path for the save file, and Windows has a limit of 260 characters for this. If you do not save skip in this case, the game will crash.

## Mechanic
Saving is handled ingame as a menu, if you press E/Esc(the inventory button) at the right timing you can close this menu while sleeping and the game skips the saving process, making sleeping quicker. This is a more precise input on 1.3, however it is still possible. You can alteratively close the menu by doing [WSC](/glitches/Window%20Shift%20Cancel.md) and then shutting the now open settings menu.
Typically this makes the player wake up at the farmhouse door instead of in the bed, unless you have not left the house since the save was loaded, or passed out outside the house. On 1.3, you always wake up in the bed.
This is a 1 frame input, however if you miss it and hold the menu key it still speeds up the save process.

## Methods
- E/Esc - Hold down the menu key after the fade to black is complete after pressing yes to sleep is finished, this is a wider window prior to 1.3.
- WSC - WSC after the fade to black is complete and shut the settings menu.


# Journal Control
## Notes
- Works in versions 1.0 - 1.4.

## Mechanic
If you mouse click the journal icon in the top right of the screen, you can open it regardless of the situation, for example in:
- the fade to black/fade back in when going through loadzones(this saves about 0.5s ish in allowing you to move earlier).
- After teleporting using a warp totem animation.
As a side effect, if you have a menu open as you enter an area, you cannot be put in a cutscene, this lets you e.g. avoid being hit by the Demetrius and Marnie cutscenes on the farm.

On versions 1.0 - 1.2 if you open and close the journal as you are passing out, e.g. from it being 2am, the player stands back up and you can extend the day. The player will then try to passout on the next tick, but you can indefinetly repeat this process to extend the day.

# Pause Fishing
## Notes
- Works in versions 1.0 - 1.2.

## Mechanic
If you open the journal while casting the fishing rod, the game will be paused, but the fishing bite time still counts down. You can then close the journal and start the fishing minigame from a mouse click. Note the journal will be covering the screen so you will be forced to only use audio cues for knowing if you have a fishing ring.


# Cutscene Crashing
## Notes 
- Works in version 1.5.
- Prior to 1.5 there was no safety handling in the code and the game would crash.
- 1.6 refactored how items are injected during dialogue and fixed the crash properly.

## Mechanic
This is explained with an example in the route document for [Joja Movie Theater](/routes/NDE-Glitched%20Joja%20Movie%20Theater.md), however the core mechanic is that when the game attempts to parse something of the form `anything][`, the first thing the game does is check if the dialogue starts with a `]`, which it doesn't. Then it finds there is a `[` in the dialogue, so looks for a closing `]` to match it, and it attempts to get what is in between the two characters. This results in the game attempting to get a substring of negative length, which fails, and the game falls into the error handling for the cutscene, which autoends it.

# Chest Duping
## Notes
- Works on version 1.4

## Mechanic
If you have a full inventory, and pick something up out of a chest, when you click the inventory sort button the stack size of that item will double. If the stack size goes over 999, it keeps going regardless, but will appear as multiple "linked" stacks of items that if you interact with most ways will just delete themselves and you will be left with eg 1 stack of 24 instead.

The item stacks unlink if you can seperate them into different inventories, for example putting one stack in chest A and a second in chest B, or you can safely ship the stacks one at a time into the shipping bin without them merging. 

# Stardrop Duplication
## Notes
- Works on versions 1.0 - 1.2
- Requires three stardrops

## Mechanic
1) Build a chest (preferably next to the shipping bin) and make sure that the shipping bin has no return item.
2) Place the Stardrops in the chest and remove them by right-clicking then left-clicking to remove 1 and then the rest.
3) Interacting with the shipping bin will cause the selected hotbar item to become a stack of Stardrops 2 less than the original stack and starts the eating a Stardrop cutscene, you can regain control/cancel out this cutscene either via WSC or journal control.
4) Repeat until enough Stardrops have been acquired.
any other item into the shipping bin, and then place the Stardrops in the bin to sell them without triggering the cutscene.

