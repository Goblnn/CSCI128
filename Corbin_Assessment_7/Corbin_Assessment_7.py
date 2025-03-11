# Corbin Mitchell
# CSCI 128 – Section K
# Assessment 7
# References: no one
# Time: 30 minutes



def process_inventory(items, current_inventory, inventory_delta):
    for i in range(len(items)):
        if (current_inventory[i] + inventory_delta[i]) < 0:
            current_inventory[i] = 0
        else:
            current_inventory[i] = current_inventory[i] + inventory_delta[i]

def process_sale(items, current_inventory, item, quantity_request):
    inventoryLocale = items.index(item)
    if quantity_request > current_inventory[inventoryLocale]:
        sold = current_inventory[inventoryLocale]
        current_inventory[inventoryLocale] = 0
    else:
        sold = quantity_request
        current_inventory[inventoryLocale] = current_inventory[inventoryLocale] - quantity_request
    return f"{items[inventoryLocale]} {sold}"

def generate_eod_report(items, closing_inventory, prices, running_sales_report):
    report_list = [] # Make report_list
    running_sales_string = " ".join(running_sales_report) # Make a string containg all values in running_sales_report seperated by spaces
    running_sales_report2 = running_sales_string.split(" ") # Remove all spaces to make a list of [item, price, item, price], no list in list
    for i, name in enumerate(items): # Start loop with index "i" and name of item "name"
        if name not in running_sales_report2: # if you didnt sell the item, sold nothing
            sold = 0
        else: # if you sold stuff
            sold = int(running_sales_report2[running_sales_report2.index(name) + 1]) # add the amount of items sold to a sold variable
        report_list.append(f"{name}: Inventory: {closing_inventory[i]} ${prices[i] * closing_inventory[i]:.2f} Sold: {sold} ${prices[i] * sold:.2f}") # append the output to the array created originally
    return report_list # return the array