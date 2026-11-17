#This python program is made to automatically change a human-readable paste into an optimized, fits inside text-box paste.
#Features included: 
#   Comments: single line with //blah and multiline with /* blah blah */
#   Variables: declare a variable with ///Variable myFavoriteVar
#   Preambles: If there exists multiple ///PASTE files, each one gets formatted and only that after it. Additionally, any text before a ///START command gets ignored.
#   Chickens: Doing ///MARNIE makes the paste use a reduced with.
#   Languages: All languages are supported, but admittedly only Chinese has been stress tested (and even then there is sometimes not understood nuances)
#   Gender: True Gender is Female, and False Gender is Male. You can also do ///BOY and ///GIRL in the paste to set it.
#   Optimizations: There are various optimization methods split into different functions.
import pandas as pd
import re
from Util import getFilePaths
import json

global pixelWidths
pixelWidths = dict()
global validQualifiers
validQualifiers = set()
def getValidItemsToQualify() -> None:
    global validQualifiers
    with open(r'glitchResources/ItemData/Objects.json','r',encoding='utf-8') as f:
        data = json.load(f)
        validQualifiers = set(data.keys())

def updateWidths(language:str = 'zh') -> None:
    if not language in {"ru","pt","es","de","fr","it","tr","hu","en","zh","ja","ko"}:
        raise Exception(f'{language} is not a supported language by stardew.')
    if language in ["ru","pt","es","de","fr","it","tr","hu"]:
        language = "en"
    global pixelWidths
    charDataAll = pd.read_csv(r'glitchResources/character_widths.csv',on_bad_lines='warn',encoding='utf-8')
    charDataLang = charDataAll[charDataAll['lang'] == language][['char','width']]
    charDataLang = pd.concat([charDataLang,pd.DataFrame.from_dict(_hardCodedEntries(language))])
    charDataLang.set_index('char',inplace=True)
    pixelWidths = charDataLang.to_dict()['width']
    return

def _hardCodedEntries(language:str) -> dict:
    # if the language is wrong here, it literally doesnt matter, this just looks prettier.
    match (language):
        case "zh":
            return {'char': [',','"'], 'width' :[6,11]}
        case "ja":
            return {'char':[',','"'],'width':[12,12]}
        case _:
            return {'char':[',','"'],'width':[8,10]}


updateWidths()

def lastLineLength(string:str):
    #Calculates the width of the last line in the paste
    #Note: ø is a hardcoded empty-character, whose functionality is to guard functional newlines.
    lastLine = string.split('\n')[-1]
    length = 0
    for item in lastLine:
        if item!='ø':
            length+=pixelWidths[item] -1
    length+=1
    return(length)

def makeLegal(string:str,gender:bool = True, width:int = 171) -> str:
    #Automatically adds gender switch blocks to make a name fit in the current lange
    #A False gender is male, a True gender is female, and the default width of 171 is the width of the player name textbox. 159 is the width of the pet/animal names.
    string+='\n'
    splitChar = '¦' if pixelWidths['¦'] < pixelWidths['^'] else '^'
    if gender:
        gStr = '${\n'+splitChar+'}$'
    else:
        gStr = '${'+splitChar+'\n}$'
    output = []
    i = 0
    tempOutput = ''
    while i < len(string):
        tempOutput += string[i]
        if string[i] == '\n':
            output.append(tempOutput)
            tempOutput = ''
            i+=1
            continue
        if lastLineLength(tempOutput+gStr.split('\n')[0])>width:
            nextNewLine = string.index('\n',i)
            if lastLineLength(tempOutput+string[i+1:nextNewLine]) <= width:
                tempOutput += string[i+1:nextNewLine+1]
                i = nextNewLine + 1
                continue
            output.append(tempOutput[:-1])
            output.append(gStr.split('\n')[0]+'\n')
            tempOutput = gStr.split('\n')[1]+string[i]
        i+=1
    output.append(tempOutput)
    return(''.join(output))

def removeLines(string:str, width:int = 171) -> str:
    #Automatically removes all newline characters that are not necessary for the name to fit
    #Any newline character surrounded by ø characters (as in ø\nø) is considered functional and is not trimmed.
    string = re.sub(r' +',' ',string) #probably redunent but still
    currentVersion = string.split('\n')
    i = len(currentVersion)-1
    while i > 0:
        if currentVersion[i].startswith('ø') or currentVersion[i-1].endswith('ø'):
            i-=1
            continue
        if lastLineLength(currentVersion[i-1] + currentVersion[i]) <= width:
            currentVersion[i-1] = currentVersion[i-1] + currentVersion[i]
            currentVersion[i] = '' #removed merged lines empty and remove all empty lines later(pop(k) is O(n-k),vs doing 1 O(n) operation later)
        i-=1
    return('\n'.join(line for line in currentVersion if line))

def removeQualifiers(string:str, width:int = 171) -> str:
    # Removes all (\n) item qualifiers that are not actually productive
    currentVersion = string.split('\n')
    i = 1
    while i < len(currentVersion):
        if len(currentVersion[i-1]) == 0:
            i+=1
            continue
        if currentVersion[i-1][-1] == '(' and len(currentVersion[i])>0 and currentVersion[i][0] == ')':
            if (lastLineLength(currentVersion[i-1][:-1] + currentVersion[i][1:]) <= width):
                currentVersion[i-1] = currentVersion[i-1][:-1] + currentVersion[i][1:]
                currentVersion.pop(i)
                continue
        i+=1
    return('\n'.join(currentVersion))
    
def trimComments(text:str,startingText:str = '///START') -> tuple[str,list]:
    # Removes all comments. Any text before the starting text (defaulted to ///START) is considered a preamble and removed. 
    # Multiline comments of the form /* blah blah */ is supported, along with end-of-line comments formatted as functional//Comment
    # Logs ///Variable and ///Variables declarations.
    if startingText in text:
        text = text.split('///START')[1]
    foundVariables = set()
    def _getVars(varMatch:re.Match[str]) -> str:
        args = re.split(' ',varMatch.group(0))
        if len(args) < 2:
            return ''
        nonlocal foundVariables
        foundVariables.update(args[1:])
        return ''
    text = re.sub(r'(\n|\A)///Variable(s|).*',_getVars,text,flags=re.IGNORECASE) #remove and get variables
    text = re.sub(r'//.*|/\*(\s|\S)*?\*/','',text) # remove remaining non processing

    return re.sub(r'///.*(\n|\Z)','',text),list(foundVariables) #removes remaining declarations

def lowercaseCommands(text:str) -> str:
    # Lowercases all TriggerActions and GameStateQueries, as they are case-insensitive
    # Furthermore, replaces DaysPlayed player_stat checks with days_played checks.
    triggerActions = ['NULL', 'IF', 'ADDBUFF', 'REMOVEBUFF', 'ADDMAIL', 'REMOVEMAIL', 'ADDQUEST',
 'REMOVEQUEST', 'ADDSPECIALORDER', 'REMOVESPECIALORDER', 'ADDITEM', 'REMOVEITEM', 'ADDMONEY',
 'ADDFRIENDSHIPPOINTS', 'ADDCONVERSATIONTOPIC', 'REMOVECONVERSATIONTOPIC', 'INCREMENTSTAT',
 'MARKACTIONAPPLIED', 'MARKCOOKINGRECIPEKNOWN', 'MARKCRAFTINGRECIPEKNOWN', 'MARKEVENTSEEN',
 'MARKQUESTIONANSWERED', 'MARKSONGHEARD', 'REMOVETEMPORARYANIMATEDSPRITES', 'SETNPCINVISIBLE',
 'SETNPCVISIBLE']
    gameStateQueries = ["ANY", "DATE_RANGE", "SEASON_DAY", "DAY_OF_MONTH", "DAY_OF_WEEK", "DAYS_PLAYED", "IS_GREEN_RAIN_DAY",
 "IS_FESTIVAL_DAY", "IS_PASSIVE_FESTIVAL_OPEN", "IS_PASSIVE_FESTIVAL_TODAY", "SEASON", "YEAR", "TIME", "IS_EVENT", "CAN_BUILD_CABIN",
 "CAN_BUILD_FOR_CABINS", "BUILDINGS_CONSTRUCTED", "FARM_CAVE", "FARM_NAME", "FARM_TYPE", "FOUND_ALL_LOST_BOOKS", "HAS_TARGET_LOCATION",
 "IS_COMMUNITY_CENTER_COMPLETE", "IS_CUSTOM_FARM_TYPE", "IS_HOST", "IS_ISLAND_NORTH_BRIDGE_FIXED", "IS_JOJA_MART_COMPLETE", "IS_MULTIPLAYER",
 "IS_VISITING_ISLAND", "LOCATION_ACCESSIBLE", "LOCATION_CONTEXT", "LOCATION_HAS_CUSTOM_FIELD", "LOCATION_IS_INDOORS", "LOCATION_IS_OUTDOORS",
 "LOCATION_IS_MINES", "LOCATION_IS_SKULL_CAVE", "LOCATION_NAME", "LOCATION_UNIQUE_NAME", "LOCATION_SEASON", "MUSEUM_DONATIONS", "WEATHER",
 "WORLD_STATE_FIELD", "WORLD_STATE_ID", "MINE_LOWEST_LEVEL_REACHED", "PLAYER_BASE_COMBAT_LEVEL", "PLAYER_BASE_FARMING_LEVEL",
 "PLAYER_BASE_FISHING_LEVEL", "PLAYER_BASE_FORAGING_LEVEL", "PLAYER_BASE_LUCK_LEVEL", "PLAYER_BASE_MINING_LEVEL", "PLAYER_COMBAT_LEVEL",
 "PLAYER_FARMING_LEVEL", "PLAYER_FISHING_LEVEL", "PLAYER_FORAGING_LEVEL", "PLAYER_LUCK_LEVEL", "PLAYER_MINING_LEVEL", "PLAYER_CURRENT_MONEY",
 "PLAYER_FARMHOUSE_UPGRADE", "PLAYER_GENDER", "PLAYER_HAS_ACHIEVEMENT", "PLAYER_HAS_ALL_ACHIEVEMENTS", "PLAYER_HAS_BUFF",
 "PLAYER_HAS_CAUGHT_FISH", "PLAYER_HAS_CONVERSATION_TOPIC", "PLAYER_HAS_CRAFTING_RECIPE", "PLAYER_HAS_COOKING_RECIPE",
 "PLAYER_HAS_DIALOGUE_ANSWER", "PLAYER_HAS_HEARD_SONG", "PLAYER_HAS_ITEM", "PLAYER_HAS_MAIL", "PLAYER_HAS_PROFESSION",
 "PLAYER_HAS_RUN_TRIGGER_ACTION", "PLAYER_HAS_SECRET_NOTE", "PLAYER_HAS_SEEN_EVENT", "PLAYER_HAS_TOWN_KEY", "PLAYER_HAS_TRASH_CAN_LEVEL",
 "PLAYER_HAS_TRINKET", "PLAYER_LOCATION_CONTEXT", "PLAYER_LOCATION_NAME", "PLAYER_LOCATION_UNIQUE_NAME", "PLAYER_MOD_DATA",
 "PLAYER_MONEY_EARNED", "PLAYER_SHIPPED_BASIC_ITEM", "PLAYER_SPECIAL_ORDER_ACTIVE", "PLAYER_SPECIAL_ORDER_RULE_ACTIVE",
 "PLAYER_SPECIAL_ORDER_COMPLETE", "PLAYER_KILLED_MONSTERS", "PLAYER_STAT", "PLAYER_VISITED_LOCATION", "PLAYER_FRIENDSHIP_POINTS",
 "PLAYER_HAS_CHILDREN", "PLAYER_HAS_PET", "PLAYER_HEARTS", "PLAYER_HAS_MET", "PLAYER_NPC_RELATIONSHIP", "PLAYER_PLAYER_RELATIONSHIP",
 "PLAYER_PREFERRED_PET", "RANDOM", "SYNCED_CHOICE", "SYNCED_RANDOM", "SYNCED_SUMMER_RAIN_RANDOM", "ITEM_CONTEXT_TAG", "ITEM_CATEGORY",
 "ITEM_HAS_EXPLICIT_OBJECT_CATEGORY", "ITEM_ID", "ITEM_ID_PREFIX", "ITEM_NUMERIC_ID", "ITEM_OBJECT_TYPE", "ITEM_PRICE", "ITEM_QUALITY",
 "ITEM_STACK", "ITEM_TYPE", "ITEM_EDIBILITY", "TRUE", "FALSE"]

    def _optimalCase(commandMatch:re.Match[str]) -> str:
        return commandMatch.group(0).lower().replace('m','M')

    regString = re.compile('|'.join(triggerActions+gameStateQueries),flags=re.IGNORECASE)
    text = regString.sub(_optimalCase,text)
    text = re.sub(r'player_has_Mail Any',r'player_has_Mail any',text)
    text = re.sub(r'player_stat Any',r'player_stat all',text,flags=re.IGNORECASE) #Equivalent but thinner(given unique variables per player)
    text = re.sub(r'player_stat\s+all\s+daysplayed ',r'days_played \n',text,flags=re.IGNORECASE)
    text = re.sub(r'DaysPlayed',r'daysplayed',text,flags=re.IGNORECASE) #Stats are case insensitive.
    return text

def addNewlines(text:str) -> str:
    # Automatically trims whitespace and adds newline characters around %action and %%, along with several known places for safe newlines

    def _statNameCasing(commandMatch:re.Match[str]) -> str:
            return f'{commandMatch.group(1)} {commandMatch.group('stat').lower().replace('m','M')}'
    
    text = re.sub(r'(incrementstat|(player_stat (any|all|current|Host|Target))) (?P<stat>[^ %#]+)',_statNameCasing,text,flags=re.IGNORECASE)

    def _commandNewlines(commandMatch:re.Match[str]) -> str:
        match (commandMatch.group(1)):
            case r'%action':
                return f'{commandMatch.group(1)}\n{commandMatch.group(2).strip()}\n%%\n'
            case r'%item':
                return f'{commandMatch.group(1)}{commandMatch.group(2).strip()}%%\n'
        return commandMatch.group(0)

    text = re.sub(r'(%action|%item)([\s|\S]*?)(%%\s+)',_commandNewlines,text)
    text = re.sub(r'\$action ',r'$action \n',text)

    text = re.sub(r'Received',r'\nreceived\n',text,flags=re.IGNORECASE)
    text = re.sub(r' ## ',r'\n ## \n',text)
    text = re.sub(r',',r'\n,\n',text)
    text = re.sub(r'All ',r'all\n ',text,flags=re.IGNORECASE) #theoretically could catch undeclared variables but thats a future problem
    text = re.sub(r' All',r' \nall',text,flags=re.IGNORECASE)
    text = re.sub(r' \. ',r' \n\.\n ',text)
    def _statReduction(commandMatch:re.Match[str]) -> str: #numbering is unneeded here
        return commandMatch.group(1)

    text = re.sub(r'(incrementstat [^ ]+) \s*1[^\d]',_statReduction,text,flags=re.IGNORECASE)

    text = re.sub(r'UndergroundMine',r'undergroundMine\n',text,flags=re.IGNORECASE)
    text = re.sub(r'VolcanoDungeon',r'volcanodungeon\n',text,flags=re.IGNORECASE)

    def _numberNewlines(commandMatch:re.Match[str]) -> str:
        t = commandMatch.groups()
        return f' \n{commandMatch.group(2)}{commandMatch.group(3)}\n ' if commandMatch.group(5).endswith(' ') else f' \n{commandMatch.group(2)}{commandMatch.group(3)}\n'

    text = re.sub(r'(?<!(iteM|emid|buff)) (-|)(\d+(|\.\d+))(| )',_numberNewlines,text,flags=re.IGNORECASE)
    return text

def qualifyItems(text:str) -> str:
    #AddItem commands for objects that keep functionality with non-functional itemid qualifiers
    #Example: %action additem 74%% -> %action additem (\n)74%%
    def _qualifyItem(commandMatch:re.Match[str]) -> str:
        if commandMatch.group(1) not in validQualifiers:
            return commandMatch.group(0)
        return f'additeM (\n){commandMatch.group(1)}'

    return re.sub(r'additeM +([^ \(\)%\n#]*)',_qualifyItem,text)

phrasesOfWidth = dict()
def getOfWidth(width):
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
    phrasesOfWidth[width] = [res for res in results if not 'iteM' in res] 
    return results

def getSmallNames(quantityDesired:int) -> list[str]:
    found = []
    maxWidth = 0
    while len(found) < quantityDesired:
        maxWidth += 1
        for phrase in getOfWidth(maxWidth):
            for i in range(len(phrase)): #Going to phrase+1 starts losing uniqueness, likely some kind of whitespace trimming I'm not spotting
                found.append(phrase[:i]+'√'+phrase[i:])
    return found

def measureStringOperations(text:str, gender:bool = True):
    #Assumes the cost of each string operation as the length of the resulting text
    #Sums up all string operations done, and returns the time, each individual sections time, and the final text.
    totalGenderCost = 0
    i = 0
    while True:
        try:
            startLoc = text.index('${',i)
        except ValueError:
            break
        try:
            endLoc = text.index('}$',startLoc)
        except ValueError:
            break
        contents = text[startLoc+2:endLoc]
        splitChar = "¦" if "¦" in contents else "^"
        results = contents.split(splitChar)[1] if gender else contents.split(splitChar)[0]
        text = text[:startLoc] + results + text[endLoc+2:]
        totalGenderCost+=len(text)
        i = startLoc+len(results)  
    totalActionCost = 0      
    i = 0
    while True:
        try:
            startLoc = text.index('%action',i)
        except ValueError:
            break
        try:
            endLoc = text.index('%%',startLoc)
        except ValueError:
            break
        text = text[:startLoc] + text[endLoc+2:]
        totalActionCost+=len(text)
        i = startLoc
    totalItemCost = 0
    i = 0
    while True:
        try:
            startLoc = text.index('%item',i)
        except ValueError:
            break
        try:
            endLoc = text.index('%%',startLoc)
        except ValueError:
            break
        text = text[:startLoc] + text[endLoc+2:]
        totalItemCost+=len(text)
        i = startLoc
    return(totalGenderCost+totalActionCost+totalItemCost, totalGenderCost, totalActionCost, totalItemCost, text)
        

global amountNamed
amountNamed = 0
def renameVariables(text:str,variableList:list[str]) -> str:
    #Renames all occurences of existing variables with newline-smuggling variables.
    #To avoid the same variable being used for multiple players, has a global count of the quantity used
    #Variable names that contain other variable names can cause issues; this code does its best to avoid those issues, but the warning stands.
    global amountNamed
    for item in variableList:
        for thing in variableList:
            if item!=thing and item in thing:
                print(f"Warning; you have variable names that are subsets of each other. This can cause issues. Subset; {item} and {thing}")
    newNames = getSmallNames(len(variableList) + amountNamed)[amountNamed:]
    myVL = sorted(variableList,key = lambda x: -text.count(x))
    for endingChar in ' %,':
        for i in range(len(variableList)):
            text = text.replace(' '+myVL[i]+endingChar,' '+newNames[i]+endingChar)
    for i in range(len(variableList)):
        text = text.replace(' '+myVL[i],' '+newNames[i])
    for i in range(len(variableList)):
        if myVL[i] in text:
            print("Something has gone wrong with renaming, ",i,myVL[i],newNames[i])
    amountNamed += len(variableList)
    return text

def formatText(text:str,optimize:bool = True,gender:bool = True,noFormat:bool = False, width:int = 171,verboseFormat:bool = True) -> str: 
    #171 is regular, 159 is marnie ... but 159 doesn't always work so 156?
    text = re.sub(r'\r\n|\r',r'\n',text) # standardize line ending chars
    if verboseFormat:
        print(f"The file has {len(text)} characters")
    text,declaredVariables = trimComments(text)
    text = re.sub(r' +',' ',text) #remove duplicate spaces
    if verboseFormat:
        print(f"After removing comments, we have {len(text)} characters")
    if optimize:
        text = renameVariables(text,declaredVariables)
        text = addNewlines(text)
        text = lowercaseCommands(text)
        text = qualifyItems(text)
        if verboseFormat:
            print(f"After renaming variables, we have {len(text) - text.count('ø')} characters")
    text = re.sub(r'√','ø\nø',text)  #A hardcoded shortcut for functional newline.
    if noFormat:
        return(text)
    text = re.sub(r' +',' ',text) # 2nd pass of removing double spaces
    text = makeLegal(text,gender,width)
    if verboseFormat:
        print(f"After adding gender switch blocks, we have {len(text) - text.count('ø')} characters")
    text = removeQualifiers(text, width)
    text = removeLines(text, width)
    text = re.sub(r'ø','',text)
    if verboseFormat:
        print(f"After removing all excess newlines, we have {len(text)} characters and {text.count('${')} genders, taking {measureStringOperations(text,gender)[0]} time")
    return f'{text}\n'

def processPaste(text:str,optimize:bool,gender:bool,noFormat:bool,verboseFormat:bool) -> str:
    outWidth = 156 if re.match(r'///MARNIE',text,flags=re.IGNORECASE) else 171
    outGender = gender
    if re.match(r'///GIRL',text,flags=re.IGNORECASE):
        outGender = True
    elif re.match(r'///BOY',text,flags=re.IGNORECASE):
        outGender = False

    hasNameLabel = False
    nameLabel = '' 
    def _getNameLabel(varMatch:re.Match[str]) -> str:
        nonlocal nameLabel
        nameLabel = '\n'+str(varMatch.group(0).split('///NAME')[1]).lstrip()
        nonlocal hasNameLabel
        if hasNameLabel:
            print('Warning: Multiple name labels detected, only the last one will be processed')
        hasNameLabel = True
        return ''

    text = formatText(re.sub(r'///NAME.*\n',_getNameLabel,text,flags=re.IGNORECASE),optimize,outGender,noFormat,outWidth,verboseFormat)
    return nameLabel+text

def formatFile(filePath:str,optimize:bool = True,gender:bool = True,noFormat:bool = False,verboseFormat:bool = True) -> list[str]:
    """Reads a file and compiles it into pastes.\n
        Returns list of pastes."""
    with open(filePath,encoding='utf-8') as f:
        text = f.read()
    if '///PASTE' not in text:
        text = '///PASTE' + text
    results = []
    for item in text.split('///PASTE')[1:]:
        results.append(processPaste(item,optimize,gender,noFormat,verboseFormat))
    return results

def formatToFile(filePathProxy:str,verboseFormat:bool = True,lang:str = 'zh') -> None:
    """Compiles a given input file of pastes to an output file using a (gitignored) proxy file for storing filepaths and all optimisations.\n
        filePathProxy: str - filepath to the proxy file.\n
        verboseFormat: bool - reports filesize data.\n
        lang - language to compile in, default is chinese(zh), other functionally language codes include japanese(ja) and english(en)."""
    pathIn,pathOut = getFilePaths(filePathProxy)
    formatToFileDirect(pathIn,pathOut,verboseFormat,lang)

def formatToFileDirect(inPath:str,outPath:str,verboseFormat:bool = True,lang:str = 'zh') -> None:
    """Compiles an input file to an output file of pastes using all optimisations.\n
        inPath - filePath to the input file.\n
        outPath - filePath to the output file.\n
        verboseFormat:bool - reports filesize data.\n
        lang - language to compile in, default is chinese(zh), other functionally language codes include japanese(ja) and english(en)."""
    updateWidths(lang)
    getValidItemsToQualify()
    results = formatFile(inPath,verboseFormat)
    with open(outPath,'w',encoding='utf-8') as f:
        for res in results:
            f.write(res)

def transform(paste:str) -> str:
    #Transforms an unformatted line meant for Marnie to one meant for the Mail, and vice versa.
    #Should check manually since it's imperfect.
    if '#$' in paste and r'%%' not in paste:
        paste = paste.replace('\n#$','%%\n%') #less reliable
        paste+=(r'%%')
    else:
        paste = paste.replace(r'%action','#$action')
        paste = paste.replace(r'%%','')
    return paste

if __name__ == '__main__':
#Example code that, with a file path, prints out formatted versions
    formatToFile(r'glitchResources/PathToFile.txt')
    #formatFile(r'glitchResources/PathToFile.txt', verboseFormat = False)