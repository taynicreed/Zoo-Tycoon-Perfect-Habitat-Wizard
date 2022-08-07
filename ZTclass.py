class Habitat: 
    
    def __init__(self, animal, density, foliage, rocks, minQty, maxQty):
        self.animal = animal.title()
        self.density = int(density)
        self.foliage = float(foliage)
        self.rocks = float(rocks)
        self.minQty = int(minQty)
        self.maxQty = int(maxQty)
        self.terrain = {}

    def addTerrain(self, terrType, percentage):
        self.terrain[terrType] = percentage
    
    def getMinQty(self, animal):
        return self.minQty
    
    def getMaxQty(self, animal): 
        return self.maxQty
    
    def getCageSize(self, quantity):
        return self.density * quantity

    def getTerrainDetails(self, cageSize):
        details = []
        for key, value in self.terrain.items():
            details.append(f"{key.title()}: {int(cageSize * value)} tiles")
        return details