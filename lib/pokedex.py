import csv

class Pokedex :
    pokedex = {}
    pokedexByID = {}
    pokemonTypes = {}
    typeNames = {}
    
    def __init__(self):
        with open("data/pokedex.csv", newline="") as file :
            reader = csv.DictReader(file)
            for row in reader :
                self.pokedex[row['identifier']] = int(row['species_id'])
                self.pokedexByID[int(row['species_id'])] = row['identifier']
        with open("data/types.csv", newline="") as file :
            reader = csv.DictReader(file)
            for row in reader :
                self.pokemonTypes.setdefault(int(row['pokemon_id']),set())
                self.pokemonTypes[int(row['pokemon_id'])].add(int(row['type_id']))
        with open("data/typeNames.csv",newline="") as file :
            reader = csv.DictReader(file)
            for row in reader :
                self.typeNames[int(row['type_id'])] = row['name']
        
    def convert(self, pokemonName, imageURL) :
        searchPokemonName = self.convertPGLExceptions(imageURL)
        if searchPokemonName is None :
            searchPokemonName = pokemonName.lower()
        return self.pokedex[searchPokemonName]
        
    def getType(self, pokemonID) :
        return self.pokemonTypes[pokemonID]
    
    def getTypeName(self, typeID) :
        return self.typeNames[typeID]
        
    def getAllTypeNames(self) :
        types = []
        for i in range(18) :
            types.append("")
        for key, val in self.typeNames.items() :
            types[key-1] = val
            
        return types
        
    def getName(self, pokemonID) :
        return self.pokedexByID[pokemonID]
        
    def convertPGLExceptions(self, imageURL) :
        if imageURL.endswith(".png") :
            imageURL = imageURL[:-4]
        exceptions = self.getPGLExceptions()
        if imageURL in exceptions :
            return exceptions[imageURL]
        else :
            return None
        
      
    def getPGLExceptions(self) :
        #image URL -> pokemon name
        return {
            "23f76d" : "lycanroc-midday",
            "08f76d" : "lycanroc-midnight",
            "edf76d" : "lycanroc-dusk",
            "e19271" : "wormadam-sandy",
            "c69271" : "wormadam-trash",
            "fc9271" : "wormadam-plant",
            "abb77b" : "rotom-heat",
            "90b77b" : "rotom-wash",
            "5ab77b" : "rotom-fan",
            "75b77b" : "rotom-frost",
            "3fb77b" : "rotom-mow",
            "561265" : "tornadus-therian",
            "f0684a" : "thundurus-therian",
            "bf69f9" : "landorus-therian",
            "711265" : "tornadus-incarnate",
            "0b684a" : "thundurus-incarnate",
            "da69f9" : "landorus-incarnate",
            "a47c7e" : "meowstic-female",
            "bf7c7e" : "meowstic-male",
            "595fff" : "rattata-alola",
            "f3b5e4" : "raticate-alola",
            "91b942" : "raichu-alola",
            "2c0f27" : "sandshrew-alola",
            "c6650c" : "sandslash-alola",
            "336a19" : "vulpix-alola",
            "cdbffe" : "ninetales-alola",
            "09c6ba" : "diglett-alola",
            "a41c9f" : "dugtrio-alola",
            "3e7284" : "meowth-alola",
            "d8c869" : "persian-alola",
            "81d432" : "geodude-alola",
            "1c2a17" : "graveler-alola",
            "b67ffc" : "golem-alola",
            "f286b8" : "grimer-alola",
            "8cdc9d" : "muk-alola",
            "fd8f23" : "exeggutor-alola",
            "323aed" : "marowak-alola",
            "9f9fd9" : "oricorio-pom-pom",
            "849fd9" : "oricorio-pau",
            "699fd9" : "oricorio-sensu",
            "ba9fd9" : "oricorio-baile"
        }
    