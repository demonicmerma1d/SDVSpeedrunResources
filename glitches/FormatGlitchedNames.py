#This python program is made to automatically change a human-readable paste into an optimized, fits inside text-box paste.
#Features included: 
#   Comments: single line with //blah and multiline with /* blah blah */
#   Variables: declare a variable with ///Variable myFavoriteVar
#   Preambles: Any text before a ///START command gets ignored, and formatFile further supports a ///MARNIE mode where any text after a ///MARNIE is formatted to the (narrower) chicken name widths
#   Languages: All languages are supported, but admittedly only Chinese has been stress tested (and even then there is sometimes not understood nuances)
#   Gender: True Gender is Female, and False Gender is Male. Defaults to True (as this means you get money instead of inventory clogging cookies) but supports both.
#   Optimizations: There are various optimization methods split into different functions.

global pixelWidths
pixelWidths = dict()
def updateWidths(language = 'zh'):
    #Note: Character widths is not fully understood; if you pick a non-english/chinese language, it won't be fully accurate. The scraping data, however, claimed they had identical pixel widths.
    #Call this function to chose the language used to calculate character widths; defaults to zh [chinese] as that is optimal
    if language in ["ru","pt","es","de","fr","it","tr","hu"]:
        language = "en"
    global pixelWidths
    pixelWidths = dict()
    languageFile = open('character_widths.csv')
    text = languageFile.read()
    languageFile.close()
    for item in text.split('\n'):
        if item.split(',')[0] == language:
            if ',,,' in item:
                pixelWidths[','] = int(item.split(',')[4])
            else:
                pixelWidths[item.split(',')[2]] = int(item.split(',')[3])
updateWidths()

def lastLineLength(string):
    #Calculates the width of the last line in the paste
    #Note: ø is a hardcoded empty-character, whose functionality is to guard functional newlines.
    lastLine = string.split('\n')[-1]
    length = 0
    for item in lastLine:
        if item!='ø':
            length+=pixelWidths[item] -1
    length+=1
    return(length)

def makeLegal(string,gender = True, width = 171):
    #Automatically adds gender switch blocks to make a name fit in the current lange
    #A False gender is male, a True gender is female, and the default width of 171 is the width of the player name textbox. 159 is the width of the pet/animal names, but there's some nuance I'm missing with them so I recommend using 156 instead.
    string+='\n'
    splitChar = '¦' if pixelWidths['¦'] < pixelWidths['^'] else '^'
    if gender:
        gStr = '${\n'+splitChar+'}$'
    else:
        gStr = '${'+splitChar+'\n}$'
    outPut = []
    i = 0
    tempOutput = ''
    while i < len(string):
        tempOutput += string[i]
        if string[i] == '\n':
            outPut.append(tempOutput)
            tempOutput = ''
            i+=1
        elif lastLineLength(tempOutput+gStr.split('\n')[0])>width:
            nextNewLine = string.index('\n',i)
            if lastLineLength(tempOutput+string[i+1:nextNewLine]) <= width:
                tempOutput += string[i+1:nextNewLine+1]
                i = nextNewLine + 1
            else:
                outPut.append(tempOutput[:-1])
                outPut.append(gStr.split('\n')[0]+'\n')
                tempOutput = gStr.split('\n')[1]+string[i:i+4]
                i+=4
        else:
            i+=1
    outPut.append(tempOutput)
    return(''.join(outPut))

def removeLines(string, width = 171):
    #Automatically removes all newline characters that are not necessary for the name to fit
    #Any newline character surrounded by ø characters (as in ø\nø) is considered functional and is not trimmed.
    while '  ' in string:
        string = string.replace('  ', ' ')
    currentVersion = string.split('\n')
    i = 1
    while i < len(currentVersion):
        while '  ' in currentVersion[i]:
            currentVersion[i] = currentVersion[i].replace('  ', ' ')
        if lastLineLength(currentVersion[i-1] + currentVersion[i]) <= width and not ((len(currentVersion[i-1])>0 and currentVersion[i-1][-1]=='ø') and (len(currentVersion[i]) > 0 and currentVersion[i][0]=='ø')):
            currentVersion[i-1] = currentVersion[i-1] + currentVersion[i]
            currentVersion.pop(i)
            while '  ' in currentVersion[i-1]:
                currentVersion[i-1] = currentVersion[i-1].replace('  ', ' ')
        else:
            i+=1
    return('\n'.join(currentVersion))

def removeQualifiers(string, width = 171):
    # Removes all (\n) item qualifiers that are not actually productive
    currentVersion = string.split('\n')
    i = 1
    while i < len(currentVersion):
        if len(currentVersion[i-1])>0 and currentVersion[i-1][-1] == '(' and len(currentVersion[i])>0 and currentVersion[i][0] == ')':
            if (lastLineLength(currentVersion[i-1][:-1] + currentVersion[i][1:]) <= width):
                currentVersion[i-1] = currentVersion[i-1][:-1] + currentVersion[i][1:]
                currentVersion.pop(i)
            else:
                i+=1
        else:
            i+=1
    return('\n'.join(currentVersion))
    

def trimComments(text,startingText = '///START'):
    # Removes all comments. Any text before the starting text (defaulted to ///START) is considered a preamble and removed. 
    # Multiline comments of the form /* blah blah */ is supported, along with end-of-line comments formatted as functional//Comment
    if "///START" in text:
        text = text.split('///START')[1]
    while "/*" in text:
        commentStart = text.index("/*")
        commentEnd = text.index("*/",commentStart)
        if commentEnd==-1:
            break
        text = text[:commentStart] + text[commentEnd+2:]
    newText = []
    foundVariables = []
    for line in text.split('\n'):
        newText.append(line.split('//')[0])
        if '///' in line:
            if line.split(' ')[0].split('///')[-1].lower()=='variable':
                foundVariables.append(line.split(' ')[1])
    return('\n'.join(newText),foundVariables)

def lowercaseCommands(text):
    # Lowercases all TriggerActions and GameStateQueries, as they are case-insensitive
    triggerActions = ['NULL', 'IF', 'ADDBUFF', 'REMOVEBUFF', 'ADDMAIL', 'REMOVEMAIL', 'ADDQUEST', 'REMOVEQUEST', 'ADDSPECIALORDER', 'REMOVESPECIALORDER', 'ADDITEM', 'REMOVEITEM', 'ADDMONEY', 'ADDFRIENDSHIPPOINTS', 'ADDCONVERSATIONTOPIC', 'REMOVECONVERSATIONTOPIC', 'INCREMENTSTAT', 'MARKACTIONAPPLIED', 'MARKCOOKINGRECIPEKNOWN', 'MARKCRAFTINGRECIPEKNOWN', 'MARKEVENTSEEN', 'MARKQUESTIONANSWERED', 'MARKSONGHEARD', 'REMOVETEMPORARYANIMATEDSPRITES', 'SETNPCINVISIBLE', 'SETNPCVISIBLE', 'AddBuff', 'IncrementStat', 'AddMail', 'MarkEventSeen', 'RemoveSpecialOrder', 'RemoveMail', 'RemoveItem', 'If','AddItem']
    gameStateQueries = ["ANY", "DATE_RANGE", "SEASON_DAY", "DAY_OF_MONTH", "DAY_OF_WEEK", "DAYS_PLAYED", "IS_GREEN_RAIN_DAY", "IS_FESTIVAL_DAY", "IS_PASSIVE_FESTIVAL_OPEN", "IS_PASSIVE_FESTIVAL_TODAY", "SEASON", "YEAR", "TIME", "IS_EVENT", "CAN_BUILD_CABIN", "CAN_BUILD_FOR_CABINS", "BUILDINGS_CONSTRUCTED", "FARM_CAVE", "FARM_NAME", "FARM_TYPE", "FOUND_ALL_LOST_BOOKS", "HAS_TARGET_LOCATION", "IS_COMMUNITY_CENTER_COMPLETE", "IS_CUSTOM_FARM_TYPE", "IS_HOST", "IS_ISLAND_NORTH_BRIDGE_FIXED", "IS_JOJA_MART_COMPLETE", "IS_MULTIPLAYER", "IS_VISITING_ISLAND", "LOCATION_ACCESSIBLE", "LOCATION_CONTEXT", "LOCATION_HAS_CUSTOM_FIELD", "LOCATION_IS_INDOORS", "LOCATION_IS_OUTDOORS", "LOCATION_IS_MINES", "LOCATION_IS_SKULL_CAVE", "LOCATION_NAME", "LOCATION_UNIQUE_NAME", "LOCATION_SEASON", "MUSEUM_DONATIONS", "WEATHER", "WORLD_STATE_FIELD", "WORLD_STATE_ID", "MINE_LOWEST_LEVEL_REACHED", "PLAYER_BASE_COMBAT_LEVEL", "PLAYER_BASE_FARMING_LEVEL", "PLAYER_BASE_FISHING_LEVEL", "PLAYER_BASE_FORAGING_LEVEL", "PLAYER_BASE_LUCK_LEVEL", "PLAYER_BASE_MINING_LEVEL", "PLAYER_COMBAT_LEVEL", "PLAYER_FARMING_LEVEL", "PLAYER_FISHING_LEVEL", "PLAYER_FORAGING_LEVEL", "PLAYER_LUCK_LEVEL", "PLAYER_MINING_LEVEL", "PLAYER_CURRENT_MONEY", "PLAYER_FARMHOUSE_UPGRADE", "PLAYER_GENDER", "PLAYER_HAS_ACHIEVEMENT", "PLAYER_HAS_ALL_ACHIEVEMENTS", "PLAYER_HAS_BUFF", "PLAYER_HAS_CAUGHT_FISH", "PLAYER_HAS_CONVERSATION_TOPIC", "PLAYER_HAS_CRAFTING_RECIPE", "PLAYER_HAS_COOKING_RECIPE", "PLAYER_HAS_DIALOGUE_ANSWER", "PLAYER_HAS_HEARD_SONG", "PLAYER_HAS_ITEM", "PLAYER_HAS_MAIL", "PLAYER_HAS_PROFESSION", "PLAYER_HAS_RUN_TRIGGER_ACTION", "PLAYER_HAS_SECRET_NOTE", "PLAYER_HAS_SEEN_EVENT", "PLAYER_HAS_TOWN_KEY", "PLAYER_HAS_TRASH_CAN_LEVEL", "PLAYER_HAS_TRINKET", "PLAYER_LOCATION_CONTEXT", "PLAYER_LOCATION_NAME", "PLAYER_LOCATION_UNIQUE_NAME", "PLAYER_MOD_DATA", "PLAYER_MONEY_EARNED", "PLAYER_SHIPPED_BASIC_ITEM", "PLAYER_SPECIAL_ORDER_ACTIVE", "PLAYER_SPECIAL_ORDER_RULE_ACTIVE", "PLAYER_SPECIAL_ORDER_COMPLETE", "PLAYER_KILLED_MONSTERS", "PLAYER_STAT", "PLAYER_VISITED_LOCATION", "PLAYER_FRIENDSHIP_POINTS", "PLAYER_HAS_CHILDREN", "PLAYER_HAS_PET", "PLAYER_HEARTS", "PLAYER_HAS_MET", "PLAYER_NPC_RELATIONSHIP", "PLAYER_PLAYER_RELATIONSHIP", "PLAYER_PREFERRED_PET", "RANDOM", "SYNCED_CHOICE", "SYNCED_RANDOM", "SYNCED_SUMMER_RAIN_RANDOM", "ITEM_CONTEXT_TAG", "ITEM_CATEGORY", "ITEM_HAS_EXPLICIT_OBJECT_CATEGORY", "ITEM_ID", "ITEM_ID_PREFIX", "ITEM_NUMERIC_ID", "ITEM_OBJECT_TYPE", "ITEM_PRICE", "ITEM_QUALITY", "ITEM_STACK", "ITEM_TYPE", "ITEM_EDIBILITY", "TRUE", "FALSE"]
    for action in triggerActions+gameStateQueries:
        text = text.replace(' '+action+' ',' '+action.lower().replace('m','M')+' ')
        text = text.replace('!'+action+' ','!'+action.lower().replace('m','M')+' ')
    return text

def addNewlines(text):
    # Automatically trims whitespace and adds newline characters around %action and %%, along with several known places for safe newlines
    while '%action ' in text:
        text = text.replace('%action ','%action')
    while '%% ' in text:
       text = text.replace('%% ', '%%')
    newLines = []
    for line in text.split('\n'):
        if '%action' in line: #Only %action commands have newlines trimmed, %item commands do not.
            line = line.replace('%%','\n%%\n')
        else:
            line = line.replace('%%','%%\n')
        newLines.append(line)
    text = '\n'.join(newLines)
    text = text.replace('%action','%action\n')
    text = text.replace('$action ','$action \n')
    text = text.replace("Received", "\nReceived\n")
    text = text.replace("null", "null \n")
    text = text.replace(" All ", " \nall\n ")
    text = text.replace(" Any ", " all ")
    text = text.replace(" ## ", " \n ## \n")
    return text

def qualifyAddItems(text):
    #AddItem commands for objects keep functionality with non-functional itemid qualifiers. If you're using any un-qualified non-objects, list them blow.
    #Example: %action additem 74%% -> %action additem (\n)74%%
    dontQualify = ['MiniForge','AdvancedIridiumRod',"ReturnScepter"]
    newLines = []
    for line in text.split('\n'):
        if 'additeM' in line:
            itemId = line[line.index('additeM'):].split(' ')[1]
            if itemId[0]!='(' and itemId not in dontQualify:
                line = line.replace('additeM '+itemId, 'additeM (\n)'+itemId)
        newLines.append(line)
    return '\n'.join(newLines)

phrasesOfWidth = dict()
def getOfWidth(width):
    #Gives all string combinations that are a certain width.
    if width == 0:
        return([''])
    elif width < 0:
        return()
    if width in phrasesOfWidth:
        return(phrasesOfWidth[width])
    results = []
    for char in  '!$()*+-/:;<=>?abcdefghijklMnopqrstuvwxyz|':
        for previous in getOfWidth(width - pixelWidths[char]):
             results.append(previous+char)
    if len(results)!=len(set(results)):
        print(results)
    phrasesOfWidth[width] = results
    return results
    

def getSmallNames(quantityDesired):
    #Gets a list of smaller variable names to be used instead of verbose descriptive ones.
    found = []
    maxWidth = 0
    while len(found) < quantityDesired:
        maxWidth += 1
        for phrase in getOfWidth(maxWidth):
            for i in range(len(phrase)): #Going to phrase+1 starts losing uniqueness; caused by an %action IncrementStat Var%% as ending whitespace is trimmed. If those aren't used, you can make renaming slightly better.
                found.append(phrase[:i]+'ø\nø'+phrase[i:])
    return found

def renameVariables(text,variableList):
    #Renames all occurences of existing variables with newline-smuggling variables.
    newNames = getSmallNames(len(variableList))
    myVL = sorted(variableList,key = lambda x: -text.count(x))
    for i in range(len(variableList)):
        text = text.replace(' '+myVL[i]+' ',' '+newNames[i]+' ')
    for i in range(len(variableList)):
        text = text.replace(' '+myVL[i],' '+newNames[i])
    for i in range(len(variableList)):
        if myVL[i] in text:
            print("Something has gone wrong with renaming, ",i,myVL[i],newNames[i])
    return text

def formatText(text,optimize = True,gender = True,noFormat = False, width = 171): 
    #Give it text and it will optimize it and add gender switch blocks to fit within the width.
    #171 is regular width, 159 is marnie, but 159 doesn't always work [I'm missing something] so I recommend 156.
    print(f"The file has {len(text)} characters")
    text,declaredVariables = trimComments(text)
    print(f"After removing comments, we have {len(text)} characters")
    if optimize:
        text = lowercaseCommands(text)
        text = addNewlines(text)
        text = renameVariables(text,declaredVariables)
        text = qualifyAddItems(text)
        print(f"After renanming variables, we have {len(text) - text.count('ø')} characters")
    if noFormat:
        return(text)
    text = makeLegal(text,gender, width)
    print(f"After adding gender switch blocks, we have {len(text) - text.count('ø')} characters")
    text = removeQualifiers(text, width)
    text = removeLines(text, width)
    text = text.replace('ø','')
    print(f"After removing all excess newlines, we have {len(text)} characters and {text.count('${')} genders")
    return(text)

def formatFile(filePath,optimize = True,gender = True,noFormat = False, width = 171):
    #Takes a file path and produces the formatted versions (either the entire text, or split into regular and Marnie parts)
    file = open(filePath)
    text = file.read()
    file.close()
    if '///MARNIE' in text:
        return(formatText(text.split('///MARNIE')[0],optimize,gender,noFormat, width), formatText(text.split('///MARNIE')[1],optimize,gender,noFormat, 156))
    return formatText(text,optimize,gender,noFormat, width)

#a = formatFile("/Users/alexa/Desktop/glitchperfection.txt") #Example code that, with a file path, prints out the formatted versions. You could give it the GlitchedTruePerfUnformatted files.
#if len(a)==2:
#    print(a[0])
#    print(a[1])
#else:
#    print(a)
