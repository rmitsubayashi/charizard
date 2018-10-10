import lib.fileManager as fileManager
import analyzer as analyzer
from lib.normalizer import Normalizer  

x=0
y=1

def unifyLowOccuringPokemon(xOrY):
    inputFile = fileManager.getNormalizedParties(xOrY)
    idMap = fileManager.getIDMap()
    sortedTally, tally, total = analyzer.tallyPokemonCt(xOrY)
    threshhold = 3
    first = -1
    for party in inputFile :
        for i in range(len(party)) :
            tallyCt = tally[idMap.get(party[i])]
            if tallyCt <= threshhold :
                if first == -1 :
                    print(party[i])
                    first = party[i]
                else :
                    party[i] = first
                
    return inputFile
    
def tweak() :
    Normalizer().normalizeParties()
    fileManager.savePokemonTypes(x)
    fileManager.savePokemonTypes(y)
    
    tweakedX = unifyLowOccuringPokemon(x)
    tweakedY = unifyLowOccuringPokemon(y)
    fileManager.clearNormalizedParties()
    for party in tweakedX :
        fileManager.addNormalizedParty(party, x)
    for party in tweakedY :
        fileManager.addNormalizedParty(party, y)
    print("done tweaking :)")
    
    

#tweak()
Normalizer().normalizeParties()
