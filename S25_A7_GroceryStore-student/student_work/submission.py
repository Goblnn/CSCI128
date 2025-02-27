# Isaac Lane
# CSCI 128 - Section K
# Assessment 7
# References: None
# Time: 30 minutes

def process_inventory(items, current_inventory, inventory_delta):
    for i in range(len(items)):
        current_inventory[i] += inventory_delta[i]

        if(current_inventory[i] < 0):
            current_inventory[i] = 0

def process_sale(items, current_inventory, item, quantity):
    itemIndex = items.index(item)

    itemsSold = 0

    if(quantity < 0):
        current_inventory[itemIndex] += -quantity
        itemsSold += quantity
    else:
        current_inventory[itemIndex] -= quantity

        if(current_inventory[itemIndex] < 0):
            itemsSold += quantity + current_inventory[itemIndex]
            current_inventory[itemIndex] = 0

    return f"{item} {itemsSold}"

def generate_eod_report(items, closing_inventory, prices, running_sales_report):
    eodReport = []
    totalSales = []

    for i in range(len(running_sales_report)):
        cur = running_sales_report[i].split()
        item = cur[0]
        amount = int(cur[1])
        
        if(item in totalSales):
            itemIndex = totalSales.index(item)
            priceIndex = items.index(item)

            totalSales[itemIndex + 1] += amount * prices[priceIndex]
            totalSales[itemIndex + 2] += amount
        else:
            priceIndex = items.index(item)

            totalSales.append(item)
            totalSales.append(amount * prices[priceIndex])
            totalSales.append(amount)

    i = 0
    for i in range(len(items)):
        item = items[i]
        if(item in totalSales):
            salesIndex = totalSales.index(item)
            currentStockPrice = closing_inventory[i] * prices[i]

            eodReport.append(f"{item}: Inventory: {closing_inventory[i]} ${currentStockPrice:.2f} Sold: {totalSales[salesIndex + 2]} ${totalSales[salesIndex + 1]:.2f}")
        else:
            currentStockPrice = closing_inventory[i] * prices[i]

            eodReport.append(f"{item}: Inventory: {closing_inventory[i]} ${currentStockPrice:.2f} Sold: 0 $0.00")

    return eodReport