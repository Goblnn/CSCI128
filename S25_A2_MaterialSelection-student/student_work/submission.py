# Isaac Lane
# CSCI 128 - Section K
# Assessment 2
# References: no one
# Time: 

metal = input("METAL>")
metal_list = input("PRICES>")
densities = input("DENSITIES>")
density_indices = input("DENSITY_INDICES>")
resists = input("RESISTS>")

metal_list = metal_list.split(" ")
density_indices = density_indices.split(" ")

metal_index = metal_list.index(metal)
metal_price = metal_list[metal_index + 1]
metal_density = densities[int(density_indices[0]):int(density_indices[1])+1]

