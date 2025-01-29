# Isaac Lane
# CSCI 128 - Section K
# Assessment 2
# References: no one
# Time: 1 hour

primary_bank = input("MAIN> ")
backup_bank = input("BACKUP> ")
req_type = input("TYPE> ")
req_amount = int(input("AMOUNT> "))

primary_bank = primary_bank.split(" ")
backup_bank = backup_bank.split(" ")

primary_index = (primary_bank.index(req_type))+1
backup_index = (backup_bank.index(req_type))+1

# print(type_index)

primary_amount = int(primary_bank[primary_index])
backup_amount = int(backup_bank[backup_index])
total_amount = primary_amount + backup_amount

if(total_amount < req_amount):
    print("OUTPUT Error: Amount requested exceeds reserves")
else:
    primary_remaining = primary_amount - req_amount

    if(primary_remaining <= 0):
        print("OUTPUT Warning: Main reserve depleted")
        print(f"OUTPUT Main Level: {0}")
    else:
        print(f"OUTPUT Main Level: {primary_remaining}")

    if(primary_remaining <= 0):
        backup_remaining = backup_amount - abs(primary_remaining)

        if(backup_remaining <= 0):
            print("OUTPUT Warning: Backup reserve depleted")
            print(f"OUTPUT Backup Level: {backup_remaining}")
        else:
            print(f"OUTPUT Backup Level: {backup_remaining}")
    elif(backup_amount <= 0):
        print("OUTPUT Warning: Backup reserve depleted")
        print(f"OUTPUT Backup Level: {backup_amount}")
    else:
        print(f"OUTPUT Backup Level: {backup_amount}")