import re
from collections import defaultdict
from StardewItems1_6 import Exists

whiteSpacePattern = re.compile(r'\[\s+\]')
subPatterns = [re.compile(string) for string in ['@',r'%farm',r'%favorite',r'%pet']]
percentTokens = ['%adj', '%noun', '%place', '%spouse', '%name', '%firstnameletter', '%time', '%band', '%book',
'%pet', '%farm', '%favorite', '%fork', '%year', '%kid1', '%kid2', '%revealtaste', '%season']

def ReplacePlayerEnteredStrings(baseStr:str,version:str,substitutions) -> str: 
    for i in range(len(substitutions)):
        if i > 3:
            break
        baseStr = subPatterns[i].sub(substitutions[i],baseStr)
    if version == '1.6':
        baseStr = whiteSpacePattern.sub('[]',baseStr)
    return baseStr

def crashTest1_6(baseString:str,showExpanded:bool = False,*substitutions:str) -> bool:
    expandedStr = ReplacePlayerEnteredStrings(baseString,'1.6',substitutions)
    if showExpanded:
        print(f'{expandedStr}\n')
    willCrash = '[]' in expandedStr
    print(f'Crash: {willCrash}')
    return willCrash

def renderedString1_6(baseString:str,*substitutions:str) -> tuple[str,dict[str,int]]|None: #direct reimplementation of part of dialogue.cs::prepareCurrentDialogueForDisplay()
    if baseString[:2] == '$v': return "",{}
    if '}' in baseString:
        baseString = baseString.split('}')[1]
    baseString.replace('$k','')
    isToken = False
    if baseString[0] == '%':
        for token in percentTokens:
            if baseString.startswith(token):
                isToken = True
                break
        if not isToken:
            baseString = baseString[1:]

    baseString = ReplacePlayerEnteredStrings(baseString,'1.6',substitutions)
    if not "[" in baseString:
        return baseString, {}
    items = defaultdict(int)
    notifiedForRandomItem = False
    open_index = 0
    while open_index >= 0 and open_index < len(baseString):
        open_index = baseString.index('[',max(0,open_index))
        if open_index < 0:
            continue
        try:
            close_index = baseString.index(']',open_index)
        except:
            break
        if close_index < 0:
            break
        if open_index+1 == close_index:
            print("Crash")
            return #crash
        itemIds = baseString[open_index+1:close_index].split(' ')
        fail = False
        if not notifiedForRandomItem and len(itemIds) > 1:
            print('This name generates inconsistent randomised items')
            notifiedForRandomItem = True
        for itemId in itemIds:
            itemData = Exists(itemId)
            if len(itemData) == 0:
                fail = True
                break
            items[itemData] += 1
        if fail:
            open_index += 1
            continue
        baseString = baseString[:open_index] + baseString[close_index+1:] if close_index < len(baseString) - 1 else baseString[:open_index]
    return baseString,items

def EvaluateDialogueStr1_6(baseStr:str,*substitutions:str,printFileState = True):
    variables = ['Player Name','Farm','Favorite','Pet']
    subCount = len(substitutions)
    for i in range(4):
        if i > subCount - 1:
            print(f'{variables[i]}:\nany')
        else:
            print(f'{variables[i]}:\n{substitutions[i]}')
    print('\nExpanded Name:')
    crashTest1_6(baseStr,True,*substitutions)
    res = renderedString1_6(baseStr,*substitutions)
    if res != None:
        rendered,items = res
    print(f'\nRendered Name:\n{rendered}')
    print('\nItems:')
    for key,value in items.items():
        print(f'{key}:{value}')

if __name__ == '__main__':
    baseStr = '@'
    playerName = r'3%farmet3%farmet'
    farmName = r']%favoritet%favorit'
    favoriteName = r'[279]%pet%pet%pe'
    petName = r'[857][857][857][7'
    nameInfo = [playerName,farmName,favoriteName,petName]
    EvaluateDialogueStr1_6(baseStr,*nameInfo)