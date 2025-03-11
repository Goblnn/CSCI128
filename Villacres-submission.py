# Edward Villacres
# CSCI 128 – Section K
# Assessment 7
# References: Jonathan Newberry
# Time: 7 hours 30 minutes


# Function for Process Inventory
def process_inventory(items, current_inventory, inventory_delta):
    for i in range(len(items)):
        item = items[i]
#        print(item)
        inventory = current_inventory[i]
#        print(inventory)
        delta = inventory_delta[i]
#        print(delta)
        current_inventory_updated = inventory + delta
        if current_inventory_updated >= 0:
            current_inventory[i] = inventory + delta
        else:
            current_inventory[i] = 0
    return

#Tests Function process_inventory
if __name__ == "__main__":
    items = ["banana", "apple", "orange"]
    current_inventory = [0, 5, 3]
    inventory_delta = [6, -3, -4]
    process_inventory(items, current_inventory, inventory_delta)
    print(current_inventory) # [6, 2, 0]



# Function for Process Sale
def process_sale(items, current_inventory, item, quantity):
    running_sales_report = []
    amount_sold = 0
    for i in range(len(items)):
        item_track = items[i]
#        print(item_track)
        inventory = current_inventory[i]
#        print(inventory)
        if item == item_track:
            if quantity >= inventory:
                new_inventory = 0
                amount_sold = inventory
            else:
                new_inventory = inventory - quantity
                amount_sold = quantity
            current_inventory[i] = new_inventory
            report = item, str(amount_sold)
            running_sales_report.append(report)
    return f"{item} {amount_sold}" 
          
#Tests Function process_sale
if __name__ == "__main__":
    items = ["banana", "apple", "orange"]
    current_inventory = [6, 2, 0]
    running_sales_report = []
    report = process_sale(items, current_inventory, "banana", 7)
    print(report) # banana 6
    running_sales_report.append(report)
    print(running_sales_report) # ["banana 6"]
    print(current_inventory) # [0, 2, 0]




# Function for Generate EOD Report
def generate_eod_report(items, closing_inventory, prices, running_sales_report):
    final_report = [] # make final report array
    for i in range(len(items)): # loop over all items
        item = items[i] # assign item name
        print(item) # print it
        inventory = closing_inventory[i] # get inventory of item
        print(inventory) # print it
        price = prices[i] # get price of item
        inventory_value = inventory * price # get total price of inventory currently
        item_sales = 0
        item_sold_num = 0

        for j in range(len(running_sales_report)):
#            length = len(running_sales_report)
            item_sold = running_sales_report[j]  
            item_sold_list = item_sold.split()
            print(item_sold_list)
            if item in item_sold_list:
                item_sold_num = item_sold_list[1]
#                print(item_sold_num)
                item_sales = float(item_sold_num) * price
#                print(item_sales)
     
        final_report.append(f"{item}: Inventory: {inventory} ${inventory_value:.2f} Sold: {item_sold_num} ${item_sales:.2f}")
        item_sold_num = 0    

    return final_report

#Test Function generate_eod_report
if __name__ == "__main__":
    items = ["banana", "apple", "orange"]
    current_inventory = [6, 2, 0]
    prices = [.59, 2.49, 3.39]
    running_sales_report = ["banana 5", "orange 15",]
    final_report =\
    generate_eod_report(items, current_inventory, prices, running_sales_report)
    print(final_report)



