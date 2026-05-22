import json
from functools import lru_cache

Qualifiers = ['(O)','(BC)','(F)','(W)','(B)','(H)','(M)','(P)','(S)','(T)','(TR)','(WP)','(FL)']

@lru_cache
def _getIds() -> set[str]:
    entries = set()
    dataFiles = ['Objects','BigCraftables','Furniture','Weapons','Boots','Hats','Mannequins','Pants','Shirts','Tools','Trinkets',]
    for i in range(11):
        with open(f'glitchResources/ItemData/{dataFiles[i]}.json','r') as f:
            localItemData = json.load(f)
        keys = {Qualifiers[i]+key for key in localItemData.keys()}
        entries.update(keys)
    entries.update(f'(WP){i}' for i in range(112))
    entries.update(f'(FL){i}' for i in range(88))
    return entries


@lru_cache(maxsize = 50)
def Exists(itemId:str) -> str:
    Entries = _getIds()
    itemId = itemId.strip()
    if len(itemId) == 0:
        return ''
    if itemId[0] == '(':
        if itemId in Entries:
            return itemId
    for qualifier in Qualifiers:
        if qualifier+itemId in Entries:
            return qualifier+itemId
    return ''

if __name__=='__main__':
    print(Exists('857'))

