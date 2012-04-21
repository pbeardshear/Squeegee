"""
	Consolidate css
    
"""

import sys, re

# Read in a css file by command-line argument
fileName = sys.argv[1] if len(sys.argv) > 1 else None
overwriteMode = sys.argv[2] if len(sys.argv) > 2 else None

activeTokens = []
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

def openBlock(line):
    """
    Sets up the state for a new block, if this line
    starts a new block
    """
    global openTokenBlock
    global activeTokens
    global tokens
    if re.search("{", line):
        openTokenBlock = True
        return True

def closeBlock(line):
    """
    Closes the state for a block
    """
    global openTokenBlock
    global activeTokens
    global tokens
    if re.search("}", line):
        openTokenBlock = False
        activeTokens = []
        return True

def tokenize(line):
    global activeTokens
    global openTokenBlock
    global tokens
    # Tokenize a selector string
    # Two cases: the selectors are in-lined with the styling, or they are not
    tokenList = None
    if re.match("\w", line):
        if re.search("{", line):
            # styles in this line
            arr = line.split("{")
            # We only care about the part before the open brace
            tokenList = re.split(",\s*", arr[0])
            openTokenBlock = True
        else:
            tokenList = re.split(",\s*", line)
        for selectorTree in tokenList:
            selectors = tuple(filter(None, re.split("\s*", selectorTree)))
            print "selectors", selectors
            tokens[selectors] = tokens[selectors] if selectors in tokens else ""
            activeTokens.append(selectors)
        """
        selectorTree = tuple(tokenList[i].strip() for i in range(len(tokenList)) if tokenList[i])
        print "selector tree", selectorTree
        tokens[selectorTree] = tokens[selectorTree] if selectorTree in tokens else ""       # TODO: Check if this selector already has styles, and if so don't overwrite
        activeTokens.append(selectorTree)
        """
    
def addStyles(line):
    # Add the list of styles to the current token
    global activeTokens
    global openTokenBlock
    global inLineStyles
    if openTokenBlock and activeTokens:
        # Handle stuff
        if inLineStyle:
            # Styles are inlined
            # TODO: Handle this case
            return
        else:
            for token in activeTokens:
                tokens[token] += line
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
        if closeBlock(line):
            # End of the block
            continue
        elif openBlock(line):
            # Open a new block
            continue
        # If we opened a new block, its possible that the styles are inlined
        if openTokenBlock:
            # We are inside a block, so just add the line to the current active tokens
            addStyles(line)
        else:
            # Tokenize the line
            tokenize(line)
    print tokens
    # Write the tokens back to the file
    tokens.items().sort()
    for tokens, styles in tokens.items():
        outFile.write(" ".join(tokens))
        outFile.write("\n{\n")
        outFile.write(styles)
        outFile.write("}\n")
        outFile.write("\n")
else:
    print "Please specify a path to a css file you wish to cleanup."
    

