# Mail Injection
## Mechanism
On 1.6, when the player opens their mailbox, the game does the following actions:

First, it replaces all @ symbols with the players name. Second, it applies gender switch blocks. Third, it runs Action commands. Fourth, it runs Item commands. 

Notably, as all of those special actions occur after the name gets replaced, we potentially have a *lot* of tools to play with. Unfortunately, unlike in dialogue it only replaces @ symbols, meaning that these commands are almost universally unusable in an NDE context, and so extensive use of [Dialogue Extension](/glitches/Dialogue%20Extension.md) is often required.

## Action Commands

The formatting of an action command is %action [command]%%, and it trims all leading and closing whitespace. The complete list of action commands can be found on the [wiki](https://stardewvalleywiki.com/Modding:Trigger_actions#Triggers), but the most notable ones are:

`AddItem <ID> [count] [quality]`: Allows for the adding of any item id in the game, at custom counts and (even impossible) qualities

`RemoveItem <ID> [count]`: Enables removing unnecessary items automatically, avoiding menuing and accidental clutter.

`AddBuff <ID> [duration]`: Allows for the addition of several powerful buffs.

`AddFriendshipPoints <NPC Name> <count>`: Allows for full friendship to be gained. *Does not* create friendship data, so can't be used to meet NPCs.

`AddMail All <mail id> [received/now/tomorrow]`: Allows for both the addition of mail flags and the creation of an unlimited amount of letters in the inbox.

`AddMoney <amount>`: Gives arbitrary amount of money, though is generally obsoleted by the similar item command.

`If <query> ## <action if true> [ ## <action if false>]`: Enables automatic staging of commands, allowing for different commands to be executed each read. Additionally, opens access to the GameStateQuery queries, of which some are not side-effect free.

`IncrementStat <stat key> <amount>`: Allows for the control of the 1.6 power books, along with various other special stats and the use of custom stats.

`MarkCookingRecipeKnown/MarkCraftingRecipeKnown All <recipe ID>`: Unlocks arbitrary recipes, though is generally obsoleted by the similar item command.

`MarkEventSeen All <event id>`: Effectively enables the ability to remove events that otherwise would slow gameplay, simply by marking them as already seen.

## Item Commands

The formatting of an item command is %item [command]%%, and it ignores all leading and closing spaces. The complete list of item commands can be found on the [wiki](https://stardewvalleywiki.com/Modding:Mail_data#Value), but the notable ones are

`money <amount>`: Gives arbitrary money (in an NDE context, fits giving up to 99 gold!)

`id <id> [count]`: Gives an item and a count (in an NDE context, fits 5 digits, allowing for 999 of 2-digit items or 99 of 3-digit items)

`cookingRecipe/craftingRecipe <key>`: Gives the corresponding recipe.

## Important Values
### Buffs
`AddBuff 20 -2` gives +10 attack.

`AddBuff 21 -2` makes you invincible.

`AddBuff 22 -2` gives a 2 speed boost.

`AddBuff 24 -2` is monster musk.

`AddBuff 28 -2` makes you immune to debuffs.

`AddBuff statue_of_blessings_0 -2` gives a 0.5 speed boost.

`AddBuff statue_of_blessings_1 -2` gives a luck buff.

`AddBuff statue_of_blessings_2 -2` gives unlimited energy.

`AddBuff statue_of_blessings_5 -2` increases crit chance by 10%.

### Mail Flags

ccDoorUnlock, canReadJunimoText, ccBoilerRoom, ccBulletin, ccCraftsRoom, ccFishTank, ccPantry, ccVault, ccMovieTheater, OpenedSewer, sawQiPlane, gotMaxStamina, artifactFound, communityUpgradeShortcuts, HasSkullKey, HasTownKey, HasSpecialCharm, Island_FirstParrot, ISLAND_NORTH_DIGSITE_LOAD, willyBoatFixed, and more!

### Statistics
`IncrementStat Book_Speed` makes the first Way Of The Wind automatically read, giving a 0.25 speed boost.

`IncrementStat Book_Speed2` makes the second Way Of The Wind automatically read, giving a 0.25 speed boost.

`IncrementStat Book_Grass` makes Ol' Slitherlegs be automatically read, significantly reducing grass's movement speed penalty.

`IncrementStat DaysPlayed [number]` allows you to change the value of DaysPlayed arbitrarily. This governs several events (like railroad access) but unfortunately not seasons.

`IncrementStat blessingOfWaters 999` makes all fish caught today easier.

### Queries

`If location_is_indoors UndergroundMine120` causes the side-effect of unlocking the floor 120 elevator

`If days_played <min> [max]` allows for name staging.

`If player_stat Any <stat id> <min> [max]` allows for name staging with custom variables (which could include newline characters).

### Events
`MarkEventSeen All 65` gets rid of the Demetrius intro cutscene.

`MarkEventSeen All 1590166/897405` are Marnie's cat and dog cutscenes respectively.


