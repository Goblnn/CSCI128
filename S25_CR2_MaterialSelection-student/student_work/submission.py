# CSCI 128
# Assessment 2 Code Review
# Group members names: Isaac Lane, Corbin Mitchell, Edward Villacres


#get the metal we want
metal = input("METAL> ")

#get the metal price 
price_list = input("PRICES> ").split(" ")
price_ind = price_list.index(metal) + 1
price = int(price_list[price_ind])

#get the metal density
densities = input("DENSITIES> ")
density_indices = input("DENSITY_INDICES> ").split(" ")
density = float(densities[int(density_indices[0]) : int(density_indices[1]) + 1])

#get the metal resistivity
resists = input("RESISTS> ")
metal_ind = resists.index(metal)
resist_ind = metal_ind + len(metal)
resist = float(resists[resist_ind:resist_ind+4])

weight = 3.1415 * (0.5 ** 2) * (100 * 63360) * density
total_price = weight * price
resistivity = resist * (100 * 63360) / (3.1415 * (0.5 ** 2))

print(f"OUTPUT {metal} Weight {weight:.3f}")
print(f"OUTPUT {metal} Price {total_price:0.3f}")
print(f"OUTPUT {metal} Resistivity {resistivity:0.3f}")