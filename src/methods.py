# Importing required libraries and modules
import json
import csv
import os
import pandas as pd
from datetime import datetime
import random

def loadData(filepath: str) -> dict:
    """Allows the system load data from the inventory"""
    try : 
        with open(filepath, 'r') as file :
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}

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

def generate_order_id() -> str:
    """Allows the system generate order ID"""
    return "OR" + datetime.now().strftime("%Y%m%d%H%M%S")

def apply_discount(bill: float, inventory) -> float:
    """Applying discounts on the basis of offers and festivals"""
    discount = inventory.get("*", 0)
    return bill - ((discount/100)*bill)

def custumer_details() -> tuple:
    """Custumer details validification"""
    while True:
        global custumer_name
        custumer_name = input("ENTER CUSTOMER NAME : ").strip()                    # Custumer Name
        if custumer_name.replace(" ", "").isalpha() and len(custumer_name) >= 3:
            custumer_name = custumer_name.upper()
            break
        else:
            print("INVALID NAME! USE ONLY LETTERS (MIN 3 CHARACTERS).")

    while True:
        global custumer_age
        custumer_age = input("ENTER CUSTOMER AGE : ").strip()                      # Custumer Age
        if custumer_age.isdigit() and 1 <= int(custumer_age) <= 100:
            custumer_age = int(custumer_age)
            break
        else:
            print("INVALID AGE! ENTER A NUMBER BETWEEN 1 AND 100.")

    while True:
        global custumer_gender
        custumer_gender = input("ENTER CUSTOMER GENDER (M/F) : ").strip().upper()  # Custumer Gender
        if custumer_gender in ("M", "F"):
            break
        else:
            print("INVALID GENDER! ENTER ONLY M OR F")

    return (custumer_name, custumer_age, custumer_gender)

def view_inventory(inventory) -> None:
    """Making the custumer see the inventory and choose appropriate item to buy"""
    print('\nHERE IS THE INVENTORY WITH DETAILS :\n')
    inventory_data = pd.DataFrame(inventory).T
    if inventory:
        inventory_data = inventory_data.drop(index="*")
        inventory_data = inventory_data.drop(columns=["COST"]).to_string()
    print(inventory_data) 

def add_to_cart(inventory, custumer_cart) -> None:
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

                    print(f'YOUR TOTAL BILL OF THIS ORDER WILL BE : INR {total} AFTER APPLYING {discount}% DISCOUNT.')

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

def update_item(inventory, custumer_cart) -> None:
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
        print(f'THE AMOUNT AND BILL OF THE ITEM HAS BEEN SUCCESSFULLY UPDATED! TOTAL BILL: INR{upd_bill}')

    else:
        print('SORRY! BUT THAT ITEM DOESNT EXIST IN YOUR CART!')

def remove_item(custumer_cart) -> None:
    """Section that allows the customer to remove an item from their cart"""
    rem_item = input('\nENTER THE ITEM YOU WANT TO REMOVE FROM YOUR CART: ').upper().strip()

    if rem_item in custumer_cart:
        del custumer_cart[rem_item]
        print(f'THE ITEM "{rem_item}" HAS BEEN SUCCESSFULLY REMOVED FROM YOUR CART!')
    else:
        print('SORRY! THAT ITEM DOES NOT EXIST IN YOUR CART!')

def view_my_cart(custumer_cart) -> None:
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
        print(f"\nYOUR BILL CURRENTLY IS INR {bill:.2f}")

def finalize_and_pay(inventory, custumer_cart, custumer_id, custumer_name, custumer_age, custumer_gender) -> None:
    """Final Section that deals with payment, feedback and database updatation"""

    print("\nITEMS IN YOUR CART ARE AS FOLLOWS :\n")
    cart_data = pd.DataFrame(custumer_cart).T
    cart_data = cart_data.drop(columns=["ORDER-ID"])
    cart_data = cart_data.drop(columns=["TIME"])
    print(cart_data.to_string())

    bill = 0
    for item, details in custumer_cart.items():
        bill += details["BILL"]

    final_bill = apply_discount(bill, inventory)

    print(  "\n---------------------------------------------------------------------------------------------"
            f"\nYOUR FINAL BILL AFTER APPLYING "
            f"{inventory.get("*", 0)}% SEASONAL DISCOUNT IS INR {final_bill:.2f}\n"
            f"YOU MAY PAY THE BILL AMOUNT NOW!"
            "\n---------------------------------------------------------------------------------------------\n")

    # Demo Payment Scenerio
    os.makedirs("DataBase/Payment-Bills", exist_ok=True)

    # Imporing Data to salesDB.csv
    while True :
        payment = input("IS THE PAYMENT SUCCESSFUL ? (Y/N) : ").upper().strip()
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
        if payment == "C":
            print("PAYMENT CANCELLED. NO DATA WRITTEN!")
            return
        
        if payment == "N":
            print("PAYMENT NOT CONFIRMED. TRY AGAIN OR PRESS C TO CANCEL!")

    # Updating inventory.json
    for item, details in custumer_cart.items():
            inventory[item]["STOCKS"] -= details["QUANTITY"]

    with open("src/inventory.json", "w") as f: 
            json.dump(inventory, f, indent=4)


    # Demo Payment Bill Scenerio
    cart_details = ""

    for item in custumer_cart.items():
        cart_details += (
            f"{item[0]:<18}"
            f"{item[1]['ORDER-ID']:<10}"
            f"{item[1]['QUANTITY']:^6}"
            f"INR {item[1]['PRICE']:^8.2f}"
            f"{item[1]['DISCOUNT']:^8.2f}%\t\t"
            f"INR {item[1]['BILL']:^10.2f}\n"
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
Product            Order-ID        Qty    Price     Discount          Bill
----------------------------------------------------------------------------------
{cart_details}
----------------------------------------------------------------------------------

SubTotal                           : INR {bill:.2f}
Seasonal Discount ({inventory['*']:.2f}%)          : -INR {((inventory['*']/100) * bill):.2f}
----------------------------------------------------------------------------------
TOTAL AMOUNT PAYABLE               : INR {final_bill:.2f}
----------------------------------------------------------------------------------
                    Thank You For Shopping With Us!
                    Visit Again — Have a Great Day!
----------------------------------------------------------------------------------
"""

    with open(f"DataBase/Payment-Bills/BILL-{custumer_id}.txt", "w") as f:
        f.write(bill_template)

    print(f"\nYOUR BILL HAS BEEN GENERATED SUCCESFULLY!\nYOU MAY CHECK AT \"DataBase/Payment-Bills/BILL-{custumer_id}.txt\"")

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
