def getFilePaths(filePathProxy:str) -> tuple[str,str]:
    """Reads a given (preferably gitignored for convinience) file to get input and output filepaths for other functions.
        returns the first filepath prepended with "input:" as the designated input filepath, 
        and the first filepath prepended with "out:" as the designated output filepath."""
    with open(filePathProxy,encoding='utf-8') as f:
        pastePaths = [path.rstrip() for path in f.readlines()]
    if len(pastePaths) == 0:
        raise Exception(f'no filepaths given in {filePathProxy}')
    inputPastePaths = [path[6:] for path in pastePaths if path.startswith('input:')]
    if not inputPastePaths:
        raise Exception(f'no filepath labelled as input(input:path) is in {filePathProxy}')
    outputPastePaths = [path[4:] for path in pastePaths if path.startswith('out:')]
    if not outputPastePaths:
        raise Exception(f'no filepath labelled as input(input:path) is in {filePathProxy}')
    return inputPastePaths[0],outputPastePaths[0]