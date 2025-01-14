# Isaac Lane
# CSCI 128 - Section K
# Assessment 1
# References: no one
# Time: 

name = input("NAME>")

# Development Costs
land = 145230000
equipment = 36200000
development = 209500000
infrastructure = 80700000
dam = 48100000
misc = 28200000

development_costs = land + equipment + development + infrastructure + dam + misc

print(development_costs)

# Operating Costs
excavation_price = 9
excavation_amount = 1000000

excavation_total = excavation_price * excavation_amount

processing_price = 10
processing_amount = 1000000

processing_total = processing_price * processing_amount

employee_price = 100000
employee_amount = 150

employee_total = employee_price * employee_amount

utility_price = 100000000
utility_amount = 1

utility_total = utility_price * utility_amount

operating_cost = excavation_total + processing_total + employee_total + utility_total

print(operating_cost)

# Reclamation Costs

reclamation = 150000000

# Gold Bar Calculations

gold_per_ton = 11
gold_extracted = gold_per_ton * excavation_amount

grams_gold_kept = gold_extracted * .95

print(grams_gold_kept)

gold_price = int(input("PRICE>"))

revenue = gold_price * grams_gold_kept
profit = revenue - operating_cost
total_profit = 20 * profit - development_costs - reclamation

# Output

print("OUTPUT Investment Planning Report of", name, "Mine")
print("OUTPUT ", int(development_costs))
print("OUTPUT ", int(operating_cost))
print("OUTPUT ", int(grams_gold_kept))
print("OUTPUT ", int(profit))
print("OUTPUT ", int(total_profit))