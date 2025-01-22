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


# Making into lists
metal_list = metal_list.split(" ")
density_indices = density_indices.split(" ")

# List information
metal_index = metal_list.index(metal)
metal_price = int(metal_list[metal_index + 1])
metal_density = int(densities[int(density_indices[0]):int(density_indices[1])+1])

# Resistance Finding
resist_index = resists.index(metal)
metal_resist = int(resists[resist_index+len(metal):(resist_index+len(metal))+4])

# Cable Information
radius = .5
length = 100 * 63360
pi = 3.1415
volume = pi * (radius ** 2) * length
area = pi * (radius ** 2)

# Final Calculations
weight = volume * metal_density
price = metal_price / weight
resistivity = metal_resist * (length / area)

print(f"OUTPUT {metal} Weight {weight}")
print(f"OUTPUT {metal} Price {price}")
print(f"OUTPUT {metal} Resistivity {resistivity}")