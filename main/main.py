import sys
from src.methods import *

def main() -> None:
    print('\n---------------------------WELCOME TO THE MARKET MANAGEMENT SYSTEM!---------------------------\n')

    inventory = loadData('src/inventory.json')   # System Inventory
    if not inventory:
        print("ERROR : INVENTORY NOT FOUND OR INVALID! SHUTTING DOWN THE PROGRAM!")
        sys.exit(1)

    existing_ids = get_existing_customer_ids('DataBase/custumerDB.csv')
    custumer_id = generate_customer_id(existing_ids)
    custumer_cart = {}                           # Customer Cart

    custumer_name, custumer_age, custumer_gender = custumer_details()
    print(f'\nYOUR CUSTUMER ID : {custumer_id}\n')   # Customer ID

    print(
        "COMMANDS :\n"
        "PRESS 0 FOR VIEWING THE INVENTORY\n"
        "PRESS 1 FOR ADDING AN ITEM TO CART\n"
        "PRESS 2 FOR UPDATING THE AMOUNT OF AN ITEM\n"
        "PRESS 3 FOR REMOVING AN ITEM FROM THE CART\n"
        "PRESS 4 FOR VIEWING YOUR CART WITH BILL AMOUNT\n"
        "PRESS 5 TO FINALIZE YOU SHOPPING AND PAYING BILL!"
    )

    # Main loop to make the program consistent
    while True:
        choice = input('\nENTER YOUR COMMAND : ')
        match choice:
            case '0': view_inventory(inventory)
            case '1': add_to_cart(inventory, custumer_cart)
            case '2': update_item(inventory, custumer_cart)
            case '3': remove_item(custumer_cart)
            case '4': view_my_cart(custumer_cart)
            case '5':
                if not custumer_cart:
                    print('THERE IS NOTHING IN YOUR CART! FIRST ORDER SOMETHING!')
                else:
                    finalize_and_pay(
                        inventory,
                        custumer_cart,
                        custumer_id,
                        custumer_name,
                        custumer_age,
                        custumer_gender)
                    break
            case _:
                print('INVALID INPUT! TRY AGAIN!')

try:
    main()
    
except Exception as e:
    print(f"SOMETHING WENT WRONG! {e}")
    sys.exit(1)

finally:
    print("\n---------------------------THANKS FOR VISING US! VISIT AGAIN LATER!---------------------------\n")