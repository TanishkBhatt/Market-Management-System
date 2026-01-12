# Importing required libraries and modules
import json
import csv
import pandas as pd
from datetime import datetime
import random
import qrcode

print('\n---------------------------WELCOME TO THE MARKET MANAGEMENT SYSTEM!---------------------------\n')


def loadData(filepath: str) -> dict:
    """Allows the system load data from the inventory"""
    try : 
        with open(filepath, 'r') as file :
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}


inventory = loadData('inventory.json')   # System Inventory
if not inventory:
    print("ERROR : INVENTORY NOT FOUND! SHUTTING DOWN THE PROGRAMM!\n")
    exit()


def get_existing_customer_ids(filepath: str) -> set:
    """Read existing customer IDs from CSV and return as a set"""
    ids = set()
    try:
        with open(filepath, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ids.add(row["CUSTUMER-ID"])
    except FileNotFoundError:
        pass
    return ids


def generate_customer_id(existing_ids: set) -> str:
    """Generate a new unique customer ID"""
    while True:
        cust_id = "C" + str(random.randint(1000000, 9999999))
        if cust_id not in existing_ids:
            return cust_id


def generate_order_id():
    """Allows the system generate order ID"""
    return "OR" + datetime.now().strftime("%Y%m%d%H%M%S")


existing_ids = get_existing_customer_ids('DataBase/custumerDB.csv')
custumer_id = generate_customer_id(existing_ids)

# Custumer details validification
while True:
    custumer_name = input("ENTER CUSTOMER NAME : ").strip()     # Custumer Name
    if custumer_name.replace(" ", "").isalpha() and len(custumer_name) >= 3:
        custumer_name = custumer_name.upper()
        break
    else:
        print("INVALID NAME! USE ONLY LETTERS (MIN 3 CHARACTERS).")

while True:
    custumer_age = input("ENTER CUSTOMER AGE : ").strip()       # Custumer Age
    if custumer_age.isdigit() and 1 <= int(custumer_age) <= 100:
        custumer_age = int(custumer_age)
        break
    else:
        print("INVALID AGE! ENTER A NUMBER BETWEEN 1 AND 100.")

while True:
    custumer_gender = input("ENTER CUSTOMER GENDER (M/F) : ").strip().upper()       # Custumer Gender
    if custumer_gender in ("M", "F"):
        break
    else:
        print("INVALID GENDER! ENTER ONLY M OR F.")

print(f'YOUR CUSTUMER ID : {custumer_id}')                              # Custumer ID


print('\nCOMMANDS :\nPRESS 0 FOR VIEWING THE INVENTORY\nPRESS 1 FOR ADDING AN ITEM TO CART\nPRESS 2 FOR UPDATING THE AMOUNT OF AN ITEM\nPRESS 3 FOR REMOVING AN ITEM FROM THE CART\nPRESS 4 FOR VIEWING YOUR CART WITH BILL AMOUNT\nPRESS 5 TO FINALIZE YOU SHOPPING AND PAYING BILL!')

custumer_cart = {}  # Custumer Cart

def apply_discount(bill: float):
    """Applying discounts on the basis of offers and festivals"""
    discount = inventory.get("*", 0)
    final_bill = bill - ((discount/100)*bill)
    return final_bill


def view_inventory():
    """Making the custumer see the inventory and choose appropriate item to buy"""
    print('\nHERE IS THE INVENTORY WITH DETAILS :\n')
    inventory_data = pd.DataFrame(inventory).T
    if inventory:
        inventory_data = inventory_data.drop(index="*")
        inventory_data = inventory_data.drop(columns=["COST"]).to_string()
    print(inventory_data) 


def add_to_cart():
    """Most important section of the project. Allows the custumer to add items to the custumer cart"""
    while True :
        order = input('\nENTER YOUR ORDER (PRESS * TO BREAK) : ').upper().strip()
        if order == "*":
            break

        if order in inventory:
                if order in custumer_cart:
                    print('THIS PRODUCT ALREADY EXISTS IN YOU CART. UPDATE INSTEAD!')

                elif inventory[order]["STOCKS"] == 0:
                    print('SORRY! THATS OUT OF STOCK. TRY BUYING SOMETHING ELSE.')

                else:
                    # Ask for amount until it's valid
                    while True:
                        try:
                            amount = int(input(f'ENTER THE AMOUNT YOU WANT (in {inventory[order]["UNIT"]}): '))
                            if amount < 1:
                                print('INVALID INPUT! ENTER A POSITIVE NUMBER.')
                                continue
                            if amount > inventory[order]["STOCKS"]:
                                print(f'SORRY! THE AMOUNT EXCEEDS THE STOCK LIMIT ({inventory[order]["STOCKS"]}).')
                                continue
                            break
                        except ValueError:
                            print('INVALID INPUT! ENTER AN INTEGER.')
                    
                    category = inventory[order]["CATEGORY"]
                    price = inventory[order]["PRICE"]
                    discount = inventory[order]["DISCOUNT"]
                    total = (price * amount) - ((discount/100) * (price * amount))

                    order_id = generate_order_id()

                    print(f'YOUR TOTAL BILL OF THIS ORDER WILL BE : ₹{total} AFTER APPLYING {discount}% DISCOUNT.')

                    # Custumer Cart Updatation
                    custumer_cart[order] = {
                        "ORDER-ID" : order_id,
                        "CATEGORY" : category,
                        "QUANTITY": amount,
                        "PRICE": price,
                        "DISCOUNT": discount,
                        "BILL": total,
                        "TIME": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    print('ITEMS AND ITS DETAILS SUCCESFULLY ADDED TO YOUR CART!')
        else:
            print('SORRY! NO ITEM NAMED SO FOUND.')


def update_item():
    """Section that Allows the custumer to update the amount of items from custumer cart"""
    upd_item = input('\nENTER THE ITEM WHOSE AMOUNT YOU WANNA UPDATE : ').upper().strip()

    if upd_item in custumer_cart:
        # Loop until valid updated amount is entered
        while True:
            try:
                upd_amount = int(input(f'ENTER THE UPDATED AMOUNT OF THAT ITEM : '))
                if upd_amount < 1:
                    print('INVALID AMOUNT! ENTER A POSITIVE NUMBER OR REMOVE THE ITEM FROM CART.')
                    continue

                max_available = inventory[upd_item]["STOCKS"]
                if upd_amount > max_available:
                    print(f'SORRY! BUT THAT AMOUNT EXCEEDS THE STOCK!\nTHE CURRENT STOCK IS : {max_available}')
                    continue

                break
            except ValueError:
                print('INVALID INPUT! ENTER AN INTEGER.')

        # Update cart and inventory after a valid input 
        price = custumer_cart[upd_item]["PRICE"]
        discount = custumer_cart[upd_item]["DISCOUNT"]
        upd_bill = (price * upd_amount) - ((discount / 100) * (price * upd_amount))

        custumer_cart[upd_item]["QUANTITY"] = upd_amount
        custumer_cart[upd_item]["BILL"] = upd_bill
        print(f'THE AMOUNT AND BILL OF THE ITEM HAS BEEN SUCCESSFULLY UPDATED! TOTAL BILL: ₹{upd_bill}')

    else:
        print('SORRY! BUT THAT ITEM DOESNT EXIST IN YOUR CART!')


def remove_item():
    """Section that allows the customer to remove an item from their cart"""
    rem_item = input('\nENTER THE ITEM YOU WANT TO REMOVE FROM YOUR CART: ').upper().strip()

    if rem_item in custumer_cart:
        del custumer_cart[rem_item]
        print(f'THE ITEM "{rem_item}" HAS BEEN SUCCESSFULLY REMOVED FROM YOUR CART!')
    else:
        print('SORRY! THAT ITEM DOES NOT EXIST IN YOUR CART!')


def view_my_cart():
    """Section that allows the custumer view their cart with details"""
    if not custumer_cart:
        print('THERE IS NOTHING IN YOUR CART! FIRST ORDER SOMETHING.')
    else:
        print('\nHERE IS YOUR CART WITH DETAILS :\n')
        cart_data = pd.DataFrame(custumer_cart).T
        cart_data = cart_data.drop(columns=["ORDER-ID"])
        cart_data = cart_data.drop(columns=["TIME"])
        print(cart_data.to_string()) 

        bill = 0
        for item, details in custumer_cart.items():
            bill += details["BILL"]
        print(f"\nYOUR BILL CURRENTLY IS ₹{bill:.2f}")


def finalize_and_pay():
    """Final Section that deals with payment, feedback and database updatation"""

    print("\nITEMS IN YOUR CART ARE AS FOLLOWS :\n")
    cart_data = pd.DataFrame(custumer_cart).T
    cart_data = cart_data.drop(columns=["ORDER-ID"])
    cart_data = cart_data.drop(columns=["TIME"])
    print(cart_data.to_string())

    bill = 0
    for item, details in custumer_cart.items():
        bill += details["BILL"]

    final_bill = apply_discount(bill)

    print(  "\n---------------------------------------------------------------------------------------------"
            f"\nYOUR FINAL BILL AFTER APPLYING "
            f"{inventory.get("*", 0)}% SEASONAL DISCOUNT IS ₹{final_bill:.2f}"
            "\n---------------------------------------------------------------------------------------------\n")

    # Demo Payment Scenerio
    upi_id = "demo@upi" 
    name = "Market Management System"
    upi_link = (
            f"upi://pay?"
            f"pa={upi_id}&"
            f"pn={name}&"
            f"am={final_bill}&"
            f"cu=INR&"
            f"tn=Order%20{custumer_id}"
        )
    qr = qrcode.make(upi_link)
    qr.save(f"QRCodes/PAY-{custumer_id}.png")

    print("YOUR PAYMENT QR CODE HAS BEEN GENERATED!")
    print(f"YOU MAY SCAN THE QR-CODE AT \"QRCodes/PAY-{custumer_id}.png\" FOR PAYMENT!")

    # Imporing Data to salesDB.csv
    while True :
        payment = input("\nIS THE PAYMENT SUCCESSFUL ? (Y/N) : ").upper().strip()
        if payment == "Y":
                
            with open('DataBase/custumerDB.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([custumer_id, custumer_name, custumer_age, custumer_gender])

            with open('DataBase/salesDB.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    for item, details in custumer_cart.items():
                        writer.writerow([
                                details["ORDER-ID"],
                                custumer_id,
                                item,
                                details["CATEGORY"],
                                details["QUANTITY"],
                                details["PRICE"],
                                details["DISCOUNT"],
                                details["BILL"],
                                details["TIME"]
                        ])
                    break
        else:
            print("TRY AGAIN!")

    # Updating inventory.json
    for item, details in custumer_cart.items():
            inventory[item]["STOCKS"] -= details["QUANTITY"]

    with open("inventory.json", "w") as f: 
            json.dump(inventory, f, indent=4)


    # Demo Payment Bill Scenerio
    cart_details = ""

    for item in custumer_cart.items():
        cart_details += (
            f"{item[0]:<18}"
            f"{item[1]['ORDER-ID']:<10}"
            f"{item[1]['QUANTITY']:^6}"
            f"₹{item[1]['PRICE']:^8.2f}"
            f"{item[1]['DISCOUNT']:^8.2f}%\t\t"
            f"₹{item[1]['BILL']:^10.2f}\n"
        )

    billing_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    bill_template = f"""
------------------------------------------------------------------------------
                        MEGA CITY SHOPPING MALL
                        123, Central Avenue, India
                        Phone: +91-XXXXXXXXXX
----------------------------------------------------------------------------------

Customer Name   : {custumer_name}
Customer ID     : {custumer_id}
Billing Time    : {billing_time}

----------------------------------------------------------------------------------
Product            Order-ID        Qty    Price    Discount    Bill
----------------------------------------------------------------------------------
{cart_details}
----------------------------------------------------------------------------------

SubTotal                           : ₹{bill:.2f}
Seasonal Discount ({inventory['*']:.2f}%)          : -₹{((inventory['*']/100) * bill):.2f}
----------------------------------------------------------------------------------
TOTAL AMOUNT PAYABLE               : ₹{final_bill:.2f}
----------------------------------------------------------------------------------
                    Thank You For Shopping With Us!
                    Visit Again — Have a Great Day!
----------------------------------------------------------------------------------
"""

    with open(f"Payment Bills/BILL-{custumer_id}.txt", "w", encoding="utf-8") as f:
        f.write(bill_template)

    print(f"\nYOUR BILL HAS BEEN GENERATED SUCCESFULLY!\nYOU MAY CHECK AT \"Payment Bills/BILL-{custumer_id}.txt\"")

    # Feedback Section
    try :
            ratings = float(input("\nPLEASE GIVE YOUR RATINGS TO OUR PLATFORM : "))
            if ratings < 0 :
                print("RATINGS BELOW RANGE! DEFAULT RATING : 0")
                ratings = 0.0
            if ratings > 10 :
                print("RATINGS OUT OF RANGE! DEFAULT RATING : 10")
                ratings = 10.0
    except ValueError:
            print("INVALID INPUT! DEFAULT RATINGS : 8")
            ratings = 8.0

    feedback = input("ENTER YOU FEEDBACK TO US! (OPTIONAL) : ").title().strip()

    with open('DataBase/feedbackDB.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([custumer_id,ratings,feedback])

    print("\n---------------------------THANKS FOR VISING US! VISIT AGAIN LATER!!---------------------------\n")


def main():
    """Main loop to make the program consistent"""
    while True :
        choice = input('\nENTER YOUR COMMAND : ')
        match choice:
            case '0': view_inventory()
            case '1': add_to_cart()
            case '2': update_item()
            case '3': remove_item()
            case '4': view_my_cart()
            case '5': 
                if not custumer_cart:
                    print('THERE IS NOTING IN YOUR CART! FIRST ORDER SOMETHING!')
                else:
                    finalize_and_pay()
                    break
            case _ :
                print('INVALID INPUT! TRY AGAIN!')

if __name__ == "__main__":
    main()