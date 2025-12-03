## Dialogue Extension

Each textbox has a maximum size, limiting how many characters you can fit inside of it. This limit is not an amount of characters, however, but instead the pixel width of the text. A newline character creates a new line - and thus, the width is not increased. You can't type a newline character, but you can copy paste them in. This technique is what enables the size of Glitched pastes, and this technique is what is banned in the NoDialogueExtension category.

The main limitation behind this, however, is that the newline character is still a character. So, if you would want to input a singular command that is longer than that maximum width, you would be stuck placing a newline character which potentially makes the game unable to read the command. That's where gender switch blocks come in.

### Gender Switch Blocks

In normal dialogue, when an NPC wishes to say "boy/girl" depending on the player's gender, the game uses a gender switch block. The format for such a block is `${boy text^girl text}$` or `${boy text¦girl text}$`. This can be exploited to get around the newline issue; because gender switch blocks will be filtered before the name gets evaluated, you can hide any text you don't want in the gender you aren't in - critically, the new line character (symbolized as `\n` here). This means that a powerful tactic is to have `${\n¦}$` or `${¦\n}$` whenever a newline character is needed, as this allows for arbitrary sized text with no restrictions. In addition, you could do `${¦¦\n}$` to make the name function for both genders, but that increases name size and thus lag significantly, as processing a name of length N takes the game O(N^2) time. 

### Additional Tech

Sometimes, a gender switch block is unnecessary. This is because occasionally, having a newline character in a command does not actually break it. This can be used to slightly reduce name size as a switch block adds characters, though that ability is useless the majority of the time but can be marginally useful when creating names large enough to encounter lag. TODO: Create a list of such situations.
