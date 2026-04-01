#product list
products = {
    1: {"name": "Product 1", "desc": "Diamond Bracelet", "price": 15000},
    2: {"name": "Product 2", "desc": "Handbag", "price": 5000},
    3: {"name": "Product 3", "desc": "Watch", "price": 20000},
    4: {"name": "Product 4", "desc": "Wallet", "price": 1000}
}

cart = {}
customer_profile = {}

#show all products
def show_products():
    print("\nAvailable products:")
    for pid, info in products.items():
        print(f"[{pid}] {info['name']} - {info['desc']} : ${info['price']}")

#show cart contents
def show_cart():
    if not cart:
        print("\nYour cart is empty")
        return
    print("\nCart:")
    total = 0
    for pid, qty in cart.items():
        product = products[pid]
        price = product["price"] * qty
        total += price
        print(f"- {product['name']} x{qty} = ${price}")
    print(f"Total: ${total}")

#remove items from cart
def remove_cart():
    if not cart:
        print("\nYour cart is empty")
        return
    
    show_cart()
    try:
        pid = int(input("Enter product ID to remove: "))
    except ValueError:
        print("Invalid input.")
        return

    if pid in cart:
        qty = input("Enter quantity to remove (or 'all' to remove completely): ")
        if qty.lower() == "all":
            del cart[pid]
            print(f"Removed all {products[pid]['name']} from cart")
        elif qty.isdigit():
            qty = int(qty)
            if qty >= cart[pid]:
                del cart[pid]
                print(f"Removed {qty} x {products[pid]['name']} from cart")
            else:
                cart[pid] -= qty
                print(f"Removed {qty} x {products[pid]['name']} from cart")
        else:
            print("Invalid input")
    else:
        print("Item not found in cart")

def mask_card_number(card_num:str) -> str:
    cleaned = "".join(ch for ch in card_num if ch.isdigit())
    if len(cleaned) <= 4:
        return cleaned
    masked = "*" * (len(cleaned) - 4) + cleaned[-4:]
    groups = [masked[max(0, i-4):i] for i in range(len(masked), 0, -4)]
    groups.reverse()
    return " ".join(groups)
def checkout():
    if not cart:
        print("\nYour cart is empty. Add items before checkout.")
        return

    print("\nCheckout")
    show_cart()

    # customer profile
    print("\nEnter customer details:")
    name = input("Name: ").strip()
    address = input("Address: ").strip()

    # payment method
    print("\nSelect payment method:")
    print("[1] Credit/Debit Card\n[2] Paynow\n[3] Cash on Delivery")
    pay_choice = input("Enter choice: ").strip()
    payment_methods = {"1": "Card", "2": "Paynow", "3": "Cash on Delivery"}
    payment = payment_methods.get(pay_choice, "Card")

    # extra details depending on payment, with validation
    payment_info = ""
    if payment == "Card":
        while True:
            card_input = input("Enter Credit/Debit Card Number (digits, may include spaces/dashes): ").strip()
            cleaned = "".join(ch for ch in card_input if ch.isdigit())
            # length check for card numbers
            if not cleaned.isdigit() or not (12 <= len(cleaned) <= 19):
                print("Invalid card number. Please enter 12-19 digits.")
                continue
            
            payment_info = mask_card_number(card_input)
            break

    elif payment == "Paynow":
        while True:
            phone = input("Enter Paynow Phone Number (digits, include country code if needed): ").strip()
            cleaned = "".join(ch for ch in phone if ch.isdigit())
            if not cleaned.isdigit() or not (8 <= len(cleaned) <= 15):
                print("Invalid phone number. Please enter 8-15 digits.")
                continue
            # store a nicely formatted phone (kept as cleaned digits)
            payment_info = cleaned
            break

    elif payment == "Cash on Delivery":
        payment_info = "Reminder: Prepare cash to pay deliveryman upon arrival."

    # delivery method
    print("\nDelivery Options:")
    print("[1] Pickup (Free)\n[2] Home Delivery ($10)")
    delivery_choice = input("Enter choice: ").strip()
    delivery_methods = {"1": ("Pickup", 0), "2": ("Delivery", 10)}
    delivery_mode, delivery_cost = delivery_methods.get(delivery_choice, ("Pickup", 0))

    # calculate total
    subtotal = sum(products[pid]["price"] * qty for pid, qty in cart.items())
    total = subtotal + delivery_cost

    # save customer info (store masked card / cleaned phone)
    customer_profile.update({
        "name": name,
        "address": address,
        "payment": payment,
        "payment_info": payment_info,
        "delivery": delivery_mode,
    })

    # order summary
    print("\nOrder Summary")
    print(f"Customer: {name}")
    print(f"Address: {address}")
    print(f"Payment Method: {payment}")
    if payment in ["Card", "Paynow"]:
        print(f"Payment Details: {payment_info}")
    else:
        print(payment_info) 
    print(f"Delivery: {delivery_mode} (${delivery_cost})")
    print(f"Subtotal: ${subtotal}")
    show_cart()
    print(f"Total: ${total}")
    print("Thank you for shopping with us!\n")

    # cart clearing
    cart.clear()

#main program loop
while True:
    print("\n[1] Show Products [2] Add to Cart [3] View Cart [4] Checkout [5] Remove Items [6] Quit")
    choice = input("Enter your choice: ")

    if choice == "1":
        show_products()

    elif choice == "2":
        show_products()
        items = input("Enter product IDs to add (comma separated): ")
        try:
            ids = [int(x.strip()) for x in items.split(",")]
            for pid in ids:
                if pid in products:
                    qty = input(f"Enter quantity for {products[pid]['name']}: ")
                    if qty.isdigit():
                        qty = int(qty)
                        cart[pid] = cart.get(pid, 0) + qty
                        print(f"Added {qty} x {products[pid]['name']} to cart.")
                    else:
                        print("Invalid quantity")
                else:
                    print(f"Product ID {pid} not found")
        except ValueError:
            print("Invalid input. Please enter product IDs as numbers.")

    elif choice == "3":
        show_cart()

    elif choice == "4":
        checkout()

    elif choice == "5":
        remove_cart()

    elif choice == "6":
        print("\nExiting program.")
        break

    else:
        print("Invalid option, try again")
