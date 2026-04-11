# Kent Friendship
For glitched speedruns where you need to become friends with Kent (notably True Perfection), it is bothersome to have to sleep to Year 2 to meet him. As such, there have been 2 ways discovered to become friends with Kent in year 1.

## Version Limits
Due to #$v only being added in 1.6, and the Event.currentCommand functionality being overhauled in 1.6.16, Kent PTSD is 1.6.0 -> 1.6.15 exclusive. Baby Kent with an NPC works from 1.0 -> 1.5.0 (patched in 1.5.1), and with a player from 1.3.27 (when multiplayer got added) onwards.

## The Problem

The main issue with gaining friendship with Kent in year one is the lack of an NPC called "Kent". Commands that give friendship almost always search the map for an NPC that IsVillager named Kent and that isn't EventActor, and only gives friendship to that NPC. One exception, however, is things that already have an NPC onhand. There are two ways to cause a friendship change with an NPC named Kent that already has that NPC onhand. 

## Baby Kent
This method relies upon getting a baby named Kent, and becoming friends with them. Unfortunately, this is far slower than Kent PTSD, but it's also far funnier so it needs to be noted down. FriendshipData only uses the string-name of an NPC to know the friendship. This means that, if you were to have 2 NPC's named the same thing, becoming friends with one would become friends with the other. This presents a potential loophole, with babies. 

When you have a child with an NPC, and go to name it, a BirthingEvent occurs. This makes you type out the name of the baby you want. ConcernedApe was aware of the potential trouble with two NPC's sharing names, and thus it checks if the name you type exists in Game1.characterData or in Utility.getAllCharacters. While it finds a collision, it adds a space to the end of the child's name. This means you can't have a baby named `Kent` with an NPC in year 1, but only a baby named `Kent `.

When you have a child with another player, however, a PlayerCoupleBirthingEvent occurs. This event only checks Utility.getAllCharacters, which searchs for every character that exists on the map. As Kent (and Leo) do not exist on the map until they get added, this allows you to name a baby `Kent`.

Gaining friendship with this child is equivalent to gaining friendship with Kent, and so can be used for Perfection. Unfortunately, no glitches to add friendship points work on Baby Kent (to my knowledge) and so you need to gain friendship normally, which is dreadfully slow. As such, this is not really viable for speedruns (though could be used for challenge or minmax runs).

## Kent PTSD

When an NPC asks you a question, and your response changes friendship, the game simply reuses the NPC that asked the question (because that makes a lot of sense). So, if Kent in an event (which is created by events that require Kent) asks you a question, this allows you to have an NPC named Kent with friendship being changed. Event ID 100 is an event where Jodi makes popcorn triggering Kent's PTSD, and if you give him good advice you gain 50 friendship points. Thus, do that 2500/(50 * 1.1 (friendship 101) = 46 times, and you get to 10 hearts.

This can be performed via Dialogue Injection, through the power of Marnie. Name a chicken `#$v 100 false false #`, and that can start the cutscene as many times as you want. Normal Kent PTSD, however, is quite slow (as each cutscene even played optimally takes almost a minute to complete, meaning the full cycle takes about 45 minutes). The solution, then, is Accelerated Kent PTSD.

## Accelerated Kent PTSD

Via \~magic~ we can make it so that Kent keeps asking the question over and over, and we just keep advising him that it's not Jodi's fault until we get victory. But how can we trigger this? The trick relies on Game1.eventUp, and ItemGrabMenus.

How events work is that they have a list of commands, and an integer index to the CurrentCommand. Every frame, if there is an Game1.currentEvent, it tells the event to try to run its current command. Some commands immediately increase the CurrentCommand value, but not all of them do. After all, we wouldn't want everything to happen at once. Thus, several commands only cause an increase in CurrentCommand via their end. If an event creates a dialogue box, for example, only when that dialogue box closes does CurrentCommand get incremented (and before that, the event goes "ah my current command is Speak and I have an existing dialogue box? let's just do nothing"). For a question, it asks the question, gets the response, and that response DialogueBox is in control.

A DialogueBox knows to increase CurrentCommand if Game1.eventUp is True (and it's not a festival and a couple other things). If, then, we can get Game1.eventUp to be False, this variable will not increase and thus the game just keeps trying to ask us the question. Game1.eventUp is *only set* by Game1.StartEvent (and if you get killed in checkForEvents but that's not relevant). In this situation, the function that is responsible for StartEvent is Game1.checkForEvents. checkForEvents is *only called* when entering a new location, and that's where ItemGrabMenus come in. Namely, if you have an activeClickableMenu, the game doesn't even call checkForEvents - so by having an ItemGrabMenu active when starting an Event, Game1.eventUp is never set, and DialogueBox's become incapable of incrementing CurrentCommand.

The question then becomes, though, if DialogueBoxes can't increment CurrentCommand anymore, how could we possibly get to the command we want? In Event 100 (code located in Data/Events/SamHouse.json), the question is command #107! This is quite deep in. Well, blessed be, the exact same ItemGrabMenus that were required to keep eventUp broken can be used. Namely, when you close an ItemGrabMenu (well more like close a MenuWithInventory) the CurrentCommand gets incremented. This uses Game1.currentLocation.currentEvent rather than Game1.eventUp, so it still works! So, we can use that as our main driver of CurrentCommand. By having dozens of ItemGrabMenus created and all queued up, we can keep closing them to increase CurrentCommand.

But there's still one more layer of complexity. Namely, the cutscene itself still has *other* commands that could increment CurrentCommand. One really annoying one is the Pause commands, as once they finish counting down the CurrentCommand will get incremented; and depending on how fast you click, the amount of them that get to finish counting is inconsistent. There are two solutions to this. First off, you could just tough it up. Click at a consistent speed, and if you mess up welp reset time. But that's not *great*, and so we welcome in our second strategy - break the event even further.

The 5th, 7th, 9th, and 11th commands all are move farmer commands. (The 6th/8th/10th make noise, and increment CurrentCommand immidiately, so unless you click on the 1 frame they're supposed to happen on, they're irrelevant, and I'm not even sure if that's possible + if you do, just click again before it's too late, which should happen because you're spam clicking). How a move farmer command works is that it notes down in actorPositionsAfterMove that the Farmer is supposed to go to XY spot. It then tells the player to move upwards. While actorPositionsAfterMove is not empty, then, it refuses to run any more commands. It simply waits until the Farmer gets into that location, then it increments CurrentCommand and allows commands to run again. What's really interesting is that if we close one of our numerous ItemGrabMenus, the farmer stops moving. When we close the last one, we gain movement back (likely because startEvent isn't called). This means that by closing an ItemGrabMenu while a move command is running, we can stop the cutscene from running any commands until we move into position. This then finally gets the best strategy for Accelerated Kent PTSD.

## Performing Accelerated Kent PTSD

First, we buy a chicken. This chicken has `#$v 100 false false # `at the end of it, to play the Kent cutscene. 

### Move Breaking (Consistent) Accelerated Kent PTSD
For this, the chicken gives you 95 overflow menus. From my current experiments, the best way to do this is repeat `[79]` 3312 times, as SecretNotes are unstackable but also very easy to give. You click through Marnie's dialogue, and then you get the overflow menus and the event starts.

Wait until the event has started. This happens a couple frames before the fade to black starts to fade away, but let's imagine we wait until we see something. At that point, running timings with 2.5 speed, we can count the frames of timing window (at 60fps).

57 frames of CurrentCommand 5. It goes to 7 on the first non-wood tile.

15 frames of CurrentCommand 7. It goes to 9 at 3 tiles below the fridge.

8 frames of CurrentCommand 9. It goes to 11 at 2 tiles below the fridge.

8 frames of CurrentCommand 11. It goes to 13 (thus losing your opportunity to use the consistent method) at the tile below the fridge.

We need to reach anywhere between CurrentCommand 99 and CurrentCommand 106 with our ItemGrabMenus, as there's a +1 when you move into position, with 99 is a dialogue that would stop it from working and 107 being the goal. This means you want 95 ItemGrabMenus (which is where 95 * 36 = 3420 came from; as long as your inventory isn't max upgraded and entirely empty, this will cause 95 overflow menus), and as long as you do your first click within that ~88 frame = 1.5 second window, it's guaranteed to make it to the correct command. If you're not going to press too late, you could give slightly more to hit 106 more precisely, as there are some pause commands between 100 and 106 that extra menus could skip. Only a matter of perhaps a second, though. If you press later too late, you will need to skip cutscene and try again. Beware pressing too early, as you can make the cutscene unskippable.

When every ItemGrabMenu is closed, walk up. This will allow the move command to finally finish, and soon you will be asked a question. 

### Regular (Inconsistent, slightly quicker) Accelerated Kent PTSD
For this, you need approximately 63 overflow menus, though the amount for best consistency depends on how fast you click. If the overflow menus are all gone, and Jodi is asking you a question, you need more (and means you click faster, as that indicates the cutscene had less time to perform its own incrementing). If the overflow menus are all gone, and Kent is talking, you need less (and means you click slower. It's also possible that the question gets asked once, and then goes past it. Also means you need less).

Wait until the Farmer has arrived at the fridge (so after the window for the Move Breaking version). Click as fast as you can at a relatively consistent pace, and hopefully that leads to being asked the question.

### Question Popped

The correct choice is the middle of the 3 options, i.e. "I know you're hurting... but don't blame your wife" if you're in English. Just keep clicking in that location (both to select that answer and to advance dialogue) until you reach 10 hearts. You can see the current progress by hovering over the blue/green/yellow/red/purple/stardrop circle in the corner. Once you're at 10 hearts, you can exit the cutscene by skipping (or using a warp totem, or walking out of the house, though these will activate the event again if you walk back in). 

During this questioning, it is possible to perform other actions. Reading an experience book will still function, and the question overwrites the animation meaning no time is lost to the Kent PTSD while enabling free book reading. You can also speak to the other NPC's without breaking the loop.

After repeating 46 times, you have reached 10 hearts with Kent, and the Perfection Tracker will smile upon you. If you didn't spawn in the cooking recipes, Kent will even send you the cooking recipes! The fact that even Baby Kent is capable of sending you bombs in the mail is, perhaps, concerning.
