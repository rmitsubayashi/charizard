from lib.pokedex import Pokedex
import lib.fileManager as fileManager
import operator
import matplotlib.pyplot as plt
import pandas

x = 0
y = 1

def compareDistribution2() :
    sortedTallyX, tallyX, totalX = tallyPokemonCt(x)
    sortedTallyY, tallyY, totalY = tallyPokemonCt(y)
    
    for pokemonID, tally in sortedTallyX:
        print(str(pokemonID) + ":" + str(tally))

def compareDistribution() :
    sortedTallyX, tallyX, totalX = tallyPokemonCt(x)
    sortedTallyY, tallyY, totalY = tallyPokemonCt(y)
    
    comparisonColumnLabels = ["X","Y", "Diff", "Weighted"]
    comparisonRowLabels = []
    comparisonData = []
    
    pokedex = Pokedex()
    for pokemonID, tally in sortedTallyX :
        comparisonRowLabels.append(pokedex.getName(pokemonID))
        percentageX = round(100 * tally / totalX, 2)
        if pokemonID not in tallyY :
            comparisonData.append([percentageX, "n/a", "n/a", "n/a"])
        else :
            percentageY = round(100 * tallyY[pokemonID] / totalY, 2)
            diff = round(abs(percentageX - 100 * tallyY[pokemonID] / totalY), 2)
            minXY = min(percentageX, percentageY)
            weightedDiff = round(100*diff/minXY, 2)
            comparisonData.append([percentageX, percentageY, diff, weightedDiff ])
            del tallyY[pokemonID]
    
    sortedTallyY = sorted(tallyY.items(), key=operator.itemgetter(1), reverse=True)
    for key, val in sortedTallyY:
        percentageY = round(100 * val / totalY, 2)
        comparisonData.append(["n/a",percentageY,"n/a","n/a"])
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
    xTypes, xTotal = getTypeDistribution(x)
    yTypes, yTotal = getTypeDistribution(y)
    for i in range(len(xTypes)) :
        xTypes[i] = xTypes[i] * 100 / xTotal
        
    for i in range(len(yTypes)) :
        yTypes[i] = yTypes[i] * 100 / yTotal
    labels = Pokedex().getAllTypeNames()
    
    fig = plt.figure()
    ax = plt.axes()
    
    ax.plot(labels, xTypes, label="X")
    ax.plot(labels, yTypes, label="Y")
    ax.legend()
    
    plt.show()
    
def getTypeDistribution(xOrY) :
    total = 0
    typeTallies = [0 for i in range(18)]
    pokedex = Pokedex()
    parties = fileManager.getSemiNormalizedParties(xOrY)
    for party in parties :
        for id in party :
            types = pokedex.getType(id)
            for type in types :
                typeTallies[type-1] = typeTallies[type-1] + 1
            total += 1
    
    return typeTallies, total
    

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

def printGeneralData(xOrY) :
    parties = fileManager.getSemiNormalizedParties(xOrY)
    totalPokemon = 0
    totalParties = 0
    tally = dict()
    for party in parties :
        for id in party:
            tally.setdefault(id, 0)
            tally[id] = tally[id] + 1
            totalPokemon += 1
        totalParties += 1
        
    print("Total pokemon: " + str(totalPokemon))
    print("Total parties: " + str(totalParties))
    print("Pokemon variety: " + str(len(tally)))
    
    sortedTally = sorted(tally.items(), key=operator.itemgetter(1), reverse=True)
    oneToTen = 0
    for i in range(0,10) :
        key, val = sortedTally[i]
        oneToTen += val
    print("Distribution: 1~10 " + str(round(oneToTen * 100 / totalPokemon, 2)) + " %")
    tenToThirty = 0
    for i in range(10,30) :
        key, val = sortedTally[i]
        tenToThirty += val
    print("Distribution: 11~30 " + str(round(tenToThirty * 100 / totalPokemon, 2)) + " %")
    
    thirtyToHundred = 0
    for i in range(30,100) :
        key, val = sortedTally[i]
        thirtyToHundred += val
    print("Distribution: 31~100 " + str(round(thirtyToHundred * 100 / totalPokemon, 2)) + " %")
    
    hundredToAll = 0
    for i in range(100,len(tally)) :
        key, val = sortedTally[i]
        hundredToAll += val
    print("Distribution: 100~" + str(len(tally)) + " " + str(round(hundredToAll * 100 / totalPokemon, 2)) + " %")

def printAllGeneralData() :
    print("X")
    print("-----------")
    printGeneralData(x)
    print("")
    print("Y")
    print("-----------")
    printGeneralData(y)
    
#compareTypeDistribution()