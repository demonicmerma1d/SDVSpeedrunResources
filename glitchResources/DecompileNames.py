# counter python code to FormatGlitchedNames.py for taking a textbox optimised paste and reducing it to human readable
# supported formats:
#   Single pastes: directly applying to one paste.
#   Text/markdown files: If present, seperating pastes deliminated by ``` for embedding in markdown, this can include titles and notes about each paste in between.
#   Autodetection of details: Autodetection of player gender and name/chicken status
import re
import itertools as it
from Util import getFilePaths
# constant regexes for general use
newlines = [re.compile(r'\${\n(¦|\^)}\$'),re.compile(r'\${(¦|\^)\n}\$')]
class UncompilePaste():
    def __init__(self,compiledPaste:str,usedVars:dict[str,str] = {},usedMail:dict[str,str] = {}):
        self.compiled = compiledPaste
        self.usedVars = usedVars
        self.usedMail = usedMail
        self.varCount = len(usedVars)
        self.mailCount = len(usedMail)
        self.compileGender = True
        self.decompile()
        return

    def decompile(self) -> None:
        self.removeGenderNewlines()
        self.variables = {}
        self.type = self.detectType()
        self.prettifyCommands()

    def removeGenderNewlines(self) -> None:
        for reg in newlines:
            if reg.search(self.compiled) != None:
                self.compileGender = not r'\n}' in reg.pattern
                self.compiled = reg.sub('',self.compiled)
            self.compiled = re.sub(r'\(\s*?\)','',self.compiled) # removes too much(eg (T)blah sdfgfdhs (T))
        return

    def detectType(self) -> str:
        if re.search(r'#\$',self.compiled) != None:
            return 'MARNIE'
        return ''

    def _itemCommandPretty(self,itemComm:re.Match[str]) -> str: # we can remove excess new lines later
        return '\n'+' '.join(item.strip() for item in itemComm.group(0).split()) + '\n' 

    def _actionCommandPretty(self,actionComm:re.Match[str]) -> str: # if the compiled name is full of errors it will simply crash and I do not care
        args = re.split(' ',actionComm.group(0))
        return ' '.join(str.strip(arg) for arg in args)+'\n'

    def _stripNumericNewlines(self,number:re.Match[str]) -> str:
        return re.sub(r'\n','',number.group(0))

    def _varSub1(self,actionComm:re.Match[str]) -> str:
        args = re.split(' ',actionComm.group(0))
        args[1] = self.getOrCreateMail(args[1]) if 'mail' in args[0] else self.getOrCreateVar(args[1])
        return ' '.join(str.strip(arg) for arg in args)

    def _varSub2(self,actionComm:re.Match[str]) -> str:
        args = re.split(' ',actionComm.group(0))
        args[2] = self.getOrCreateMail(args[2]) if 'mail' in args[0].lower() else self.getOrCreateVar(args[2])
        return' '.join(str.strip(arg) for arg in args)

    def _functionalNewlines(self,actionComm:re.Match[str]) -> str:
        args = args = re.split(' ',actionComm.group(0))
        args[2] = re.sub('\n','√',args[2])
        return ' '.join(args)


    def getOrCreateVar(self,compVar:str) -> str:
        if len(compVar) > 1:
            if compVar[-1:] == '\n':
                compVar = compVar[:-1]
        if not '\n' in compVar:
            return compVar
        if not compVar in self.usedVars:
            self.usedVars[compVar] = f'var{self.varCount}'
            self.varCount += 1
        return self.usedVars[compVar]

    def getOrCreateMail(self,compMail:str) -> str:
        if not '\n' in compMail:
            return compMail
        if not compMail in self.usedMail:
            self.usedMail[compMail] = f'mail{self.mailCount}'
            self.mailCount += 1
        return self.usedMail[compMail]
                

    # process commands into single lines
    def prettifyCommands(self) -> None:
        # regex for %item commands
        self.compiled = re.sub(r'%item',r'%item ',self.compiled,flags = re.IGNORECASE)
        self.compiled = re.sub(r'%item[\S\s\n\t\r\n\f.]*?%%',self._itemCommandPretty,self.compiled)

        #standardization and variable processing
        self.compiled = re.sub(r'%action(?! )',r'%action ',self.compiled,flags=re.IGNORECASE)
        self.compiled = re.sub(r'$action',r'$action ',self.compiled,flags=re.IGNORECASE)
        self.compiled = re.sub(r'(player_(stat|has_mail) +[^ ]+ +[^ ]+(?= )|(addmail|removemail) +[^ ]+ +[^ ]+(?=(%|#| |\Z)))',self._varSub2,self.compiled,flags=re.IGNORECASE)
        print(self.compiled)
        self.compiled = re.sub(r'incrementstat +[^ %#]+(?=(%|#| \d|\Z))',self._varSub1,self.compiled,flags=re.IGNORECASE)
        self.compiled = re.sub(r'\d\n|\n\d',self._stripNumericNewlines,self.compiled)
        #formatting actions to be readable
        if self.type != 'MARNIE': 
            self.compiled = re.sub(r'%action[\S\s\n\t\r\n\f.]*?%%',self._actionCommandPretty,self.compiled)
            self.compiled = re.sub(r'\n%%',r'%%',self.compiled,flags=re.IGNORECASE)
        else:
            self.compiled = re.sub(r'#\$(.|\n)+?(?=(#|\Z))',self._actionCommandPretty,self.compiled)
        #protecting functional newlines
        self.compiled = re.sub(r'SYNCED_[A-Z]* +[^ ]+ +[^ ]+(?= )',self._functionalNewlines,self.compiled,flags=re.IGNORECASE)
        #prettifying
        self.compiled = re.sub(r' +',' ',self.compiled)

        self.compiled = '\n'.join([line for line in re.split(r'\n',self.compiled) if len(str.strip(line)) > 0])

    def decompiledPaste(self) -> str:
        return self.compiled

    def gender(self) -> str:
        return ('///GIRL' if self.compileGender else '///BOY') +'\n'

    def pasteType(self) -> str:
        if self.type == '':
            return '\n'
        return f'///{self.type}\n'

    def variableReturn(self) -> str:
        out = [f'///Variables {' '.join(varBatch)}\n' for varBatch in it.batched(self.usedVars.values(),10)]
        out.extend(f'///Variables {' '.join(mailBatch)}\n' for mailBatch in it.batched(self.usedMail.values(),10))
        return ''.join(out)


    def pasteOutput(self) -> tuple[str,str]:
        return ('///PASTE\n'+self.gender()+self.pasteType()+self.variableReturn(),self.decompiledPaste())
    
def decompileToFileDirect(inputFile:str,outputFile:str) -> None:
    """Decompiles a given input file of pastes to an output file.\n
        inputFile:str - path to input file.\n
        outputFile:str - path to output file."""
    pasteBuffer = []
    with open(inputFile,'r',encoding='utf-8') as f:
        compiledPastes = f.read()
    splits = re.split(r'```\n',compiledPastes)
    if len(splits) == 1: #process as one paste 
        uncompPaste = UncompilePaste(splits[0])
        pasteBuffer.append(uncompPaste.pasteOutput())
    elif len(splits) % 2 == 0: # assume it neatly splits 
        pairedSplits = list(zip(splits[0::2],splits[1::2]))
        for header,paste in pairedSplits:
            uncompPaste = UncompilePaste(paste).pasteOutput()
            pasteBuffer.append((header+'\n'+uncompPaste[0],uncompPaste[1]))
    else:
        print('Please ensure that the file is formated consistently headerless or each paste has a header and is marked by ``` above and below each paste.')

    with open(outputFile,'w',encoding='utf-8') as f:
        for header,paste in pasteBuffer:
            f.write(header)
            f.write(paste)
    for header,paste in pasteBuffer:
        print(header)
        print(paste)

def decompileToFile(filePathProxy:str) -> None:
    """Decompiles a given input file of pastes to an output file using a (gitignored) proxy file for storing filepaths and all optimisations.\n
        filePathProxy: str - filepath to the proxy file."""
    inPath,outPath = getFilePaths(filePathProxy)
    decompileToFileDirect(inPath,outPath)
            
if __name__ == '__main__':
    trueperf = r'routes\Pastes\GlitchedTruePerfection.md'
    testpaste = r'glitchResources\WorkingPastes\testpaste.txt'
    #decompileToFileDirect(trueperf,r'glitchResources\WorkingPastes\testpastedecomp.txt')
    decompileToFile(r'glitchResources/PathToFile.txt')