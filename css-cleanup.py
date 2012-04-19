"""
	Consolidate css
    
"""

import sys, re

# Read in a css file by command-line argument
fileName = sys.argv[1] if len(sys.argv) > 1 else None
overwriteMode = sys.argv[2] if len(sys.argv) > 2 else None

currentToken = None
openTokenBlock = False
inLineStyle = False
tokens = {}

def hasSelector(line):
    """
        There is a selector on this line if
        (1) This line is non-empty and there is no ; (matches css of style: selector \n { ... })
        (2) This line is non-empty and there is a {  (matches css of style: selector { \n ... } and selector { ... }) 
    """
    return re.search("[\w{}]", line) and (re.match("(?!.*;)", line) or re.match("{", line))
    
def hasStyling(line):
    return re.match(".*:.*;", line)

def beginTokenBlock(line):
    return re.search("{", line)

def endTokenBlock(line):
    return re.search("}", line)

def tokenize(line):
    global currentToken
    global openTokenBlock
    # Tokenize a selector string
    # Two cases: the selectors are in-lined with the styling, or they are not
    tokenList = None
    if re.search("{", line):
        # styles in this line
        arr = line.split("{")
        # We only care about the part before the open brace
        tokenList = re.split(",\s*", arr[0])
        openTokenBlock = True
    else:
        tokenList = re.split(",\s*", line)
    selectorTree = tuple(tokenList[i].strip() for i in range(len(tokenList)) if tokenList[i])
    tokens[selectorTree] = "" if not openTokenBlock else " {"
    currentToken = selectorTree
    print "tokenize", currentToken
    
def addStyles(line):
    # Add the list of styles to the current token
    global currentToken
    global openTokenBlock
    global inLineStyle
    print currentToken
    if openTokenBlock and currentToken:
        # Handle stuff
        if inLineStyle:
            # Styles are inlined
            # TODO: Handle this case
            return
        else:
            print "adding to token"
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
        print line
        if endTokenBlock(line):
            print "end of block"
            currentToken = None
            openTokenBlock = False
        elif openTokenBlock:
            print "adding styles"
            print "current token", currentToken
            addStyles(line)
        elif hasSelector(line):
            print "found selector"
            currentToken = tokenize(line)
            if hasStyling(line):
                print "has styling"
                # Inlined styling
                inLineStyle = True
                addStyles(line)
                inLineStyle = False
                currentToken = None
        elif beginTokenBlock(line):
            openTokenBlock = True
        else:
            # New line or something that we can ignore
            continue
            
    # Write the tokens back to the file
    print tokens.items()
    tokenArray = tokens.items()
    tokenArray.sort()
    for token in tokenArray:
        outFile.write(",".join(token[0]) + " ")
        outFile.write(token[1])
else:
    print "Please specify a path to a css file you wish to cleanup."
    