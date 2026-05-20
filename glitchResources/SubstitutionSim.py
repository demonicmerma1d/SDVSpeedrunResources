import re
whiteSpacePattern = re.compile(r'\[\s+\]')
subPatterns = [re.compile(string) for string in ['@',r'%farm',r'%favorite',r'%pet']]

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
        print(expandedStr)
    willCrash = '[]' in expandedStr
    print(willCrash)
    return willCrash



if __name__ == '__main__':
    baseStr = '@@'
    playerName = r'73%%farm%%farm'
    farmName = r']favoritet%favoritet['
    favoriteName = r'%pet[279]%pet%pe'
    petName = r'][857][857][857]'
    crashTest1_6(baseStr,True,playerName,farmName,favoriteName,petName)
