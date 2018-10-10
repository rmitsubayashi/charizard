import lib.fileManager as fileManager

class Normalizer :
    x = 0
    y = 1
    
    #we need to normalize both x and y at the same time
    def normalizeParties(self) :
        fileManager.clearNormalizedParties()
        fileManager.clearSemiNormalizedParties()
        
        partiesX = fileManager.getRawParties(self.x)
        partiesY = fileManager.getRawParties(self.y)

        partiesX = self.removeUnfilledParties(partiesX)
        partiesY = self.removeUnfilledParties(partiesY)
        
        partiesX = self.sort(partiesX)
        partiesY = self.sort(partiesY)
        
        partiesX = self.removeDuplicates(partiesX)
        partiesY = self.removeDuplicates(partiesY)
                
        #save this version
        for party in partiesX :
            fileManager.addSemiNormalizedParty(party, self.x)
        for party in partiesY :
            fileManager.addSemiNormalizedParty(party, self.y)
        
        idMap = self.getIDMap(partiesX, partiesY)
        #so we can revert back to pokemon IDs later
        fileManager.saveIDMap(idMap)
        partiesX = self.squishPokemonIDs(partiesX, idMap)
        partiesY = self.squishPokemonIDs(partiesY, idMap)
            
        #save final version
        for party in partiesX :
            fileManager.addNormalizedParty(party, self.x)
        
        for party in partiesY :
            fileManager.addNormalizedParty(party, self.y)
            
        print("normalized parties :)")
        
    #ポケモン数が6以下
    def removeUnfilledParties(self, arr) :
        newArr = []
        for party in arr :
            if len(party) == 5 :
                newArr.append(party)
                
        return newArr
        
    def sort(self, arr) :
        for party in arr :
            party.sort()
        return arr
    
    #make sure the arrays are sorted first
    def removeDuplicates(self, arr) :
        newArr = []
        duplicates = set()
        for party in arr :
            if str(party) not in duplicates :
                newArr.append(party)
                duplicates.add(str(party))
        return newArr
    
    #squish the pokemon IDs so they are in consecutive order
    #   ex: 1,2,4,6 -> 0,1,2,3
    def getIDMap(self, partiesX, partiesY) :
        allIDs = set()
        for party in partiesX :
            for id in party :
                allIDs.add(id)
        for party in partiesY :
            for id in party :
                allIDs.add(id)
        sortedIDs = sorted(allIDs)
        vals = []
        valLen = len(allIDs)
        for i in range(valLen) :
            vals.append(i)
        idMap = dict(zip(sortedIDs, vals))
        
        return idMap
        
    def squishPokemonIDs(self, arr, idMap) :
        newArr = []
        for party in arr :
            tempParty = []
            for id in party :
                normalizedID = idMap[id]
                tempParty.append(normalizedID)
            newArr.append(tempParty)
        return newArr
        
        
        
        
    def testFunctions(self) :
        testArrs = [[1,3,2],[3,2,1],[1,2,4]]
        sorted = self.sort(testArrs)
        assert(sorted[0] == [1,2,3])
        assert(sorted[1] == [1,2,3])
        assert(sorted[2] == [1,2,4])
        
        removeDuplicates = self.removeDuplicates(sorted)
        assert(len(removeDuplicates) == 2)
        assert (removeDuplicates[1] != [1,2,3])
        
        testArrs = [[1,4,5]]
        testArrs2 = []
        idMap = self.getIDMap(testArrs,testArrs2)
        squished = self.squishPokemonIDs(testArrs, idMap)
        assert(squished[0] == [0,1,2])
        
        testArrs = [[1,2,3,4,5], [1,2,3,4]]
        removeUnfilled = self.removeUnfilledParties(testArrs)
        assert(len(removeUnfilled) == 1)
        
        print("Normalizer functions all tests passed")
        