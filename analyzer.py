from pokedex import Pokedex
import fileManager
import operator
import matplotlib.pyplot as plt
import pandas

x = 0
y = 1

def compareDistribution() :
    sortedTallyX, tallyX, totalX = tallyPokemonCt(x)
    sortedTallyY, tallyY, totalY = tallyPokemonCt(y)
    
    comparisonColumnLabels = ["X","Y", "Diff"]
    comparisonRowLabels = []
    comparisonData = []
    
    pokedex = Pokedex()
    for pokemonID, tally in sortedTallyX :
        comparisonRowLabels.append(pokedex.getName(pokemonID))
        percentageX = 100 * tally / totalX
        if pokemonID not in tallyY :
            comparisonData.append([percentageX, "n/a", "n/a"])
        else :
            comparisonData.append([percentageX, 100 * tallyY[pokemonID] / totalY, abs(percentageX - 100 * tallyY[pokemonID] / totalY) ])
            del tallyY[pokemonID]
    
    sortedTallyY = sorted(tallyY.items(), key=operator.itemgetter(1), reverse=True)
    for key, val in sortedTallyY:
        comparisonData.append(["n/a",100 * val / totalY,"n/a"])
        comparisonRowLabels.append(pokedex.getName(key))
    
    #without setting the max rows, we can't display all rows
    pandas.options.display.max_rows = 999999
    print(pandas.DataFrame(comparisonData, comparisonRowLabels, comparisonColumnLabels))

def compareRankings() :
    sortedTallyX, tallyX, totalX = tallyPokemonCt(x)
    sortedTallyY, tallyY, totalY = tallyPokemonCt(y)
    
    yRankings = dict()
    for i in range(len(sortedTallyY)):
        key, val = sortedTallyY[i]
        yRankings[key] = i
        
    comparisonRowLabels = []
    comparisonData = [] 
    pokedex = Pokedex()    
    for i in range(len(sortedTallyX)):
        key, val = sortedTallyX[i]
        if key in tallyY :
            comparisonRowLabels.append(pokedex.getName(key))
            comparisonData.append([i,yRankings[key], abs(i-yRankings[key])])
       
    comparisonColumnLabels = ["X","Y", "Diff"]
    #without setting the max rows, we can't display all rows
    pandas.options.display.max_rows = 999999
    print(pandas.DataFrame(comparisonData, comparisonRowLabels, comparisonColumnLabels))   

def compareTypeDistribution() :
    xTypes = getTypeDistribution(x)
    for typeCt in xTypes :
        print(typeCt)
    
    print("----")
    yTypes = getTypeDistribution(y)
    for typeCt in yTypes :
        print(typeCt)
    
def getTypeDistribution(xOrY) :
    typeTallies = [0 for i in range(18)]
    pokedex = Pokedex()
    parties = fileManager.getSemiNormalizedParties(xOrY)
    for party in parties :
        for id in party :
            types = pokedex.getType(id)
            for type in types :
                typeTallies[type-1] = typeTallies[type-1] + 1
    
    return typeTallies
    

def tallyPokemonCt(xOrY) :
    parties = fileManager.getSemiNormalizedParties(xOrY)
    tally = dict()
    total = 0
    for party in parties :
        for id in party:
            tally.setdefault(id, 0)
            tally[id] = tally[id] + 1
            total += 1
        
    sortedTally = sorted(tally.items(), key=operator.itemgetter(1), reverse=True)
        
    return sortedTally, tally, total

compareTypeDistribution()            
