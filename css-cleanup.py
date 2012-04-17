"""
	Consolidate css
    
"""

import sys, re

# Read in a css file by command-line argument
fileName = sys.argv[1] if len(sys.argv) > 1 else None
overwriteMode = sys.argv[2] if len(sys.argv) > 2 else None

currentToken = None
tokens = {}

def hasSelector(line):
    # TODO: Fix this
    return re.match("(?!.*:.*;)", line)
    
def endSelector(line):
    return re.search("}", line)

def tokenize(line):
    global currentToken
    # Tokenize a selector string
    # Two cases: the selectors are in-lined with the styling, or they are not
    tokenList = None
    if re.search("{", line):
        # styles in this line
        arr = line.split("{")
        # We only care about the part before the open brace
        tokenList = re.split(",\s*", arr[0])        
    else:
        tokenList = re.split(",\s*", line)
    selectorTree = tuple(tokenList[i].strip() for i in range(len(tokenList)) if tokenList[i])
    tokens[selectorTree] = ""
    currentToken = selectorTree
    
def addStyles(line):
    # Add the list of styles to the current token
    global currentToken
    if currentToken:
        # Handle stuff
        if hasSelector(line):
            # Styles are inlined
            arr = line.split("{")
            print 'current token', currentToken
            tokens[currentToken] += "{ " + arr[1]
        else:
            print 'current token', currentToken
            tokens[currentToken] += line
    else:
        # We can't do anything
        return

if fileName and re.match("^.*\.css$", fileName):
    inFile = open(fileName, "r")
    outFile = None
    # Consolidate the css
    if overwriteMode and re.match("^-o$", overwriteMode.match):
        # Overwrite the file
        print "overwriting file"
    else:
        # Open a new file for writing
        outFile = open(re.match("^(.*)\.css$", fileName).groups()[0] + "_clean.css", "w")
    for line in inFile:
        print 'has a selector', hasSelector(line)
        if hasSelector(line):
            # Tokenize the line
            tokenize(line)
        if endSelector(line):
            currentToken = None;
        # Consolidate the styling for this line
        addStyles(line)
    # Write the tokens back to the file
    print tokens.items()
    tokenArray = tokens.items()
    tokenArray.sort()
    for token in tokenArray:
        outFile.write(",".join(token[0]) + " ")
        outFile.write(token[1])
else:
    print "Please specify a path to a css file you wish to cleanup."
    