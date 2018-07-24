

x = 0
y = 1
        
def getPageNumber(xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "pageNumberX.txt"
    elif xOrY == y:
        fileName = "pageNumberY.txt"
    else :
        print("page number xOrY invalid")
        return
       
    with open(fileName, "r") as file :
        return int(file.readline())

def savePageNumber(num, xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "pageNumberX.txt"
    elif xOrY == y:
        fileName = "pageNumberY.txt"
    with open(fileName, "w") as file :
        file.write(num)
        
def getPokemonCache() :
    pokemonCache = {}
    with open("pokemonCache.txt","r") as file :
        for line in file :
            keyVal = line.split(":")
            pokemonCache[keyVal[0]] = int(keyVal[1])
    return pokemonCache
    
def addPokemonToCache(image, id) :
    with open("pokemonCache.txt","a") as file :
        line = image + ":" + str(id) + "\n"
        file.write(line)

def getRawParties(xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "rawPartiesX.txt"
    elif xOrY == y:
        fileName = "rawPartiesY.txt"
    else :
        print("page number xOrY invalid")
        return
    parties = []
    with open(fileName,"r") as inputFile :
        for line in inputFile :
            #remove last comma
            if line.endswith(",") :
                line = line[:-1]
            ids = line.split(",")
            idsInt = []
            for idStr in ids :
                #convert to int so we can sort
                id = int(idStr)
                idsInt.append(id)
            parties.append(idsInt)
            
    return parties 
    
def getSemiNormalizedParties(xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "semiNormalizedPartiesX.txt"
    elif xOrY == y:
        fileName = "semiNormalizedPartiesY.txt"
    else :
        print("page number xOrY invalid")
        return
    parties = []
    with open(fileName,"r") as inputFile :
        for line in inputFile :
            #remove last comma
            if line.endswith(",") :
                line = line[:-1]
            ids = line.split(",")
            idsInt = []
            for idStr in ids :
                #convert to int so we can sort
                id = int(idStr)
                idsInt.append(id)
            parties.append(idsInt)
            
    return parties 

def getNormalizedParties(xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "normalizedPartiesX.txt"
    elif xOrY == y:
        fileName = "normalizedPartiesY.txt"
    else :
        print("page number xOrY invalid")
        return
    parties = []
    with open(fileName,"r") as inputFile :
        for line in inputFile :
            #remove last comma
            if line.endswith(",") :
                line = line[:-1]
            ids = line.split(",")
            idsInt = []
            for idStr in ids :
                #convert to int so we can sort
                id = int(idStr)
                idsInt.append(id)
            parties.append(idsInt)
            
    return parties 

def addRawParty(pokemonIDs, xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "rawPartiesX.txt"
    elif xOrY == y:
        fileName = "rawPpartiesY.txt"
    else :
        print("page number xOrY invalid")
        return
    with open(fileName, "a") as file :
        line = ""
        for pokemonID in partyPokemonIDs :
            line = line + str(pokemonID) + ","
        #remove last comma
        line = line[:-1]
        file.write(line)
        file.write("\n")

def addSemiNormalizedParty(pokemonIDs, xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "semiNormalizedPartiesX.txt"
    elif xOrY == y:
        fileName = "semiNormalizedPartiesY.txt"
    else :
        print("page number xOrY invalid")
        return
    with open(fileName, "a") as file :
        line = ""
        for id in pokemonIDs :
            line = line + str(id) + ","
        #remove last comma
        line = line[:-1]
        file.write(line)
        file.write("\n")
        
def addNormalizedParty(pokemonIDs, xOrY) :
    fileName = ""
    if xOrY == x:
        fileName = "normalizedPartiesX.txt"
    elif xOrY == y:
        fileName = "normalizedPartiesY.txt"
    else :
        print("page number xOrY invalid")
        return
    with open(fileName, "a") as file :
        line = ""
        for id in pokemonIDs :
            line = line + str(id) + ","
        #remove last comma
        line = line[:-1]
        file.write(line)
        file.write("\n")
        
#lists the pokemon types in order.
#make sure we've already reordered the pokemon IDs before doing this
def savePokemonTypes(xOrY) :
    outputFileName = ""
    if xOrY == x :
        outputFileName = "pokemonTypesX.txt"
    if xOrY == y :
        outputFileName = "pokemonTypesY.txt"
    inputFileName = getFileName(xOrY)
    with open(inputFileName, "r") as inputFile, open(outputFileName, "w") as outputFile :
        pokedex = Pokedex()
        for line in inputFile :
            #remove last comma
                if line.endswith(",") :
                    line = line[:-1]
                ids = line.split(",")
                idsInt = []
                for idStr in ids :
                    id = int(idStr)
                    types = poekdex.getType(id)
                    types = sorted(types)
                    line = ""
                    for type in types :
                        line = line + str(type) + ","
                    #remove last comma
                    line = line[:-1]
                    outputFile.write(line)
                    outputFile.write("\n")
            
            
def getIDMap() :
    idMap = dict()
    with open("idMap.txt","r") as file :
        for line in file:
            keyVal = line.split(",")
            key = int(keyVal[0])
            val = int(keyVal[1])
            idMap[key] = val
    return idMap            

def saveIDMap(idMap) :
    with open("idMap.txt","w") as file :
        for key, val in idMap.items():
            file.write(str(val)+","+str(key)+"\n"  )  

