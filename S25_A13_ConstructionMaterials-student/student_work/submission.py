# Isaac Lane
# CSCI 128 - Section K
# Assessment 13
# References: None
# Time: 1 hours

class Material:
    def __init__(self, ID):
        self.price = 0
        self.materialType = "Not Determined"
        self.setID(ID)

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        return self.price
    
    def setMaterialType(self, materialType):
        self.materialType = materialType

    def getMaterialType(self):
        return self.materialType
    
    def setID(self, ID):
        self.ID = ID

    def getID(self):
        return self.ID
    
class ConstructionSite:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.price = 0
        self.materials = []

    def addMaterial(self, Material):
        self.materials.append(Material)

    def getMaterials(self):
        return self.materials

    def findMaterial(self, ID):
        for material in self.materials:
            if ID == material.getID():
                return material
        return -1
    
    def calculatePrice(self):
        price = 0

        for material in self.materials:
            price += material.getID()

        self.price = price

    def countMaterials(self):
        numMats = [0,0,0]

        for material in self.materials:
            if material.getMaterialType() == "WOOD":
                numMats[0] += 1
            elif material.getMaterialType() == "STEEL":
                numMats[1] += 1
            elif material.getMaterialType() == "BRICK":
                numMats[2] += 1

        return numMats
    
    def incorporateSite(self, site):
        for material in site.getMaterials():
            self.materials.append(material)

        self.calculatePrice()

    def __str__(self):
        totalMats = 0

        matsList = self.countMaterials()
        
        for num in matsList:
            totalMats += num

        return f"{self.name} site in {self.city} has {totalMats} materials, with a value of {self.calculatePrice()}."
    
if __name__ == "__main__":
    site1File = input()
    site2File = input()

    with open("site1File", "r") as file:
        name1 = file.readline()
        city1 = file.readline()

        site1 = ConstructionSite(name1, city1)

        for line in file:
            newLine = line.split()

            newMat = Material(newLine[0])
            newMat.setMaterialType(newLine[1])
            newMat.setPrice(newLine[2])

            site1.addMaterial(newMat)

    with open("site2File", "r") as file:
        name2 = file.readline()
        city2 = file.readline()

        site2 = ConstructionSite(name2, city2)

        for line in file:
            newLine = line.split()

            newMat = Material(newLine[0])
            newMat.setMaterialType(newLine[1])
            newMat.setPrice(newLine[2])

            site2.addMaterial(newMat)

    print(f"OUTPUT {site1}")
    mats = site1.countMaterials()
    print(f"OUTPUT WOOD: {mats[0]} Steel: {mats[1]} Brick: {mats[2]}")