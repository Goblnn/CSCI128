class Animal:
    def __init__(self, species, name):
        self.species = species
        self.name = name


zoo = {}
simba = Animal("Lion" , "Simba" )
nala = Animal("Lion" , "Nala" )
timon = Animal("Meerkat" ,"Timon" )
pumbaa = Animal("Warthog" ,"Pumbaa" )
zoo[simba.species] = simba
zoo[nala.species] = nala
zoo[timon.species] = timon
zoo[pumbaa.species]=pumbaa

for animal in zoo.values():
    print(animal.name)