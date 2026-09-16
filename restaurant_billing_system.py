"""
=====================================================================
                    RESTAURANT BILLING SYSTEM
=====================================================================
A console-based Restaurant Billing System built in Python.

Features:
    1. Display Menu      - Shows categorized food items with prices
    2. Take Orders       - Lets the customer add items & quantities
    3. Calculate Bill    - Computes subtotal, tax and grand total
    4. Apply Discount    - Applies slab-based / coupon discounts
    5. Print Receipt     - Generates a neatly formatted final bill

Project Team (4 Members):
    Member 1 - Menu Design & Display Module
    Member 2 - Order Taking & Cart Management Module
    Member 3 - Bill Calculation & Discount Module
    Member 4 - Receipt Generation & Testing

Final Year Python Project
=====================================================================
"""

import datetime
import random

# ---------------------------------------------------------------
# GLOBAL CONFIGURATION
# ---------------------------------------------------------------
RESTAURANT_NAME = "The Spice Route"
RESTAURANT_ADDRESS = "Shop No. 12, MG Road, Pune - 411001"
RESTAURANT_PHONE = "+91 98765 43210"
GST_RATE = 0.05          # 5% Goods & Services Tax
RECEIPT_WIDTH = 46       # Width of the printed receipt


class MenuItem:
    """Represents a single item on the restaurant menu."""

    def __init__(self, item_id, name, category, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price


class RestaurantBillingSystem:
    """Core class that ties together menu, orders, billing and receipts."""

    def __init__(self):
        self.menu = self._build_menu()
        self.cart = {}   # {item_id: quantity}

    # -----------------------------------------------------------
    # MODULE 1: MENU (Member 1)
    # -----------------------------------------------------------
    @staticmethod
    def _build_menu():
        """Builds and returns the restaurant menu as a dictionary."""
        items = [
            (101, "Veg Spring Roll",       "Starters",   150),
            (102, "Paneer Tikka",          "Starters",   190),
            (103, "Chicken Wings",         "Starters",   220),
            (201, "Paneer Butter Masala",  "Main Course",240),
            (202, "Dal Makhani",           "Main Course",190),
            (203, "Butter Chicken",        "Main Course",280),
            (301, "Butter Naan",           "Breads",      45),
            (302, "Tandoori Roti",         "Breads",      30),
            (401, "Veg Biryani",           "Rice",       210),
            (402, "Chicken Biryani",       "Rice",       260),
            (501, "Gulab Jamun (2 pcs)",   "Desserts",    80),
            (502, "Ice Cream Scoop",       "Desserts",    70),
            (601, "Masala Chaas",          "Beverages",   50),
            (602, "Cold Coffee",           "Beverages",   90),
        ]
        return {i[0]: MenuItem(*i) for i in items}

    def display_menu(self):
        """Prints the full menu grouped by category."""
        print("\n" + "=" * RECEIPT_WIDTH)
        print(f"{RESTAURANT_NAME.upper():^{RECEIPT_WIDTH}}")
        print("MENU CARD".center(RECEIPT_WIDTH))
        print("=" * RECEIPT_WIDTH)

        categories = sorted(set(item.category for item in self.menu.values()))
        for category in categories:
            print(f"\n-- {category} --")
            print(f"{'ID':<6}{'Item':<26}{'Price':>10}")
            for item in self.menu.values():
                if item.category == category:
                    print(f"{item.item_id:<6}{item.name:<26}"
                          f"Rs.{item.price:>7.2f}")
        print("\n" + "=" * RECEIPT_WIDTH)

    # -----------------------------------------------------------
    # MODULE 2: TAKE ORDER (Member 2)
    # -----------------------------------------------------------
    def add_item_to_cart(self, item_id, quantity):
        """Adds a validated item + quantity to the cart."""
        if item_id not in self.menu:
            print(" Invalid Item ID. Please check the menu again.")
            return False
        if quantity <= 0:
            print(" Quantity must be greater than zero.")
            return False

        self.cart[item_id] = self.cart.get(item_id, 0) + quantity
        print(f" Added {quantity} x {self.menu[item_id].name} to your order.")
        return True

    def take_order(self):
        """Interactive loop that lets the user build their order."""
        print("\n--- TAKE ORDER ---")
        print("Enter the Item ID from the menu to order.")
        print("Type 0 when you are done ordering.\n")

        while True:
            try:
                item_id = int(input("Enter Item ID (0 to finish): "))
            except ValueError:
                print(" Please enter a valid numeric Item ID.")
                continue

            if item_id == 0:
                break

            try:
                quantity = int(input("Enter Quantity: "))
            except ValueError:
                print(" Please enter a valid quantity.")
                continue

            self.add_item_to_cart(item_id, quantity)

        if not self.cart:
            print("\nNo items were ordered.")

    # -----------------------------------------------------------
    # MODULE 3: CALCULATE BILL & DISCOUNT (Member 3)
    # -----------------------------------------------------------
    def calculate_subtotal(self):
        """Returns the subtotal (before tax/discount) of the cart."""
        return sum(self.menu[i].price * qty for i, qty in self.cart.items())

    @staticmethod
    def apply_discount(subtotal, coupon_code=None):
        """
        Applies slab-based discount on the subtotal.
        Rules:
            Bill > Rs.1500          -> 15% off
            Bill > Rs.1000          -> 10% off
            Bill > Rs.500           -> 5%  off
            Coupon 'WELCOME10'      -> Flat 10% off (overrides slab if better)
        Returns: (discount_amount, discount_percent)
        """
        slab_percent = 0
        if subtotal > 1500:
            slab_percent = 15
        elif subtotal > 1000:
            slab_percent = 10
        elif subtotal > 500:
            slab_percent = 5

        coupon_percent = 10 if coupon_code and coupon_code.upper() == "WELCOME10" else 0
        final_percent = max(slab_percent, coupon_percent)
        discount_amount = (subtotal * final_percent) / 100
        return round(discount_amount, 2), final_percent

    def calculate_bill(self, coupon_code=None):
        """
        Calculates the full bill breakdown.
        Returns a dictionary with subtotal, discount, tax and total.
        """
        subtotal = self.calculate_subtotal()
        discount_amount, discount_percent = self.apply_discount(subtotal, coupon_code)
        taxable_amount = subtotal - discount_amount
        tax_amount = round(taxable_amount * GST_RATE, 2)
        grand_total = round(taxable_amount + tax_amount, 2)

        return {
            "subtotal": round(subtotal, 2),
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "tax_amount": tax_amount,
            "grand_total": grand_total,
        }

    # -----------------------------------------------------------
    # MODULE 4: PRINT RECEIPT (Member 4)
    # -----------------------------------------------------------
    def print_receipt(self, bill, customer_name="Guest"):
        """Prints a neatly formatted final receipt."""
        order_id = random.randint(1000, 9999)
        now = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")

        line = "-" * RECEIPT_WIDTH
        print("\n" + "=" * RECEIPT_WIDTH)
        print(f"{RESTAURANT_NAME.upper():^{RECEIPT_WIDTH}}")
        print(f"{RESTAURANT_ADDRESS:^{RECEIPT_WIDTH}}")
        print(f"{'Ph: ' + RESTAURANT_PHONE:^{RECEIPT_WIDTH}}")
        print("=" * RECEIPT_WIDTH)
        print(f"Order ID : {order_id}")
        print(f"Customer : {customer_name}")
        print(f"Date/Time: {now}")
        print(line)
        print(f"{'Item':<20}{'Qty':>5}{'Rate':>9}{'Amount':>12}")
        print(line)

        for item_id, qty in self.cart.items():
            item = self.menu[item_id]
            amount = item.price * qty
            print(f"{item.name:<20}{qty:>5}{item.price:>9.2f}{amount:>12.2f}")

        print(line)
        print(f"{'Subtotal':<34}Rs.{bill['subtotal']:>9.2f}")
        if bill["discount_percent"] > 0:
            print(f"{'Discount (' + str(bill['discount_percent']) + '%)':<34}"
                  f"-Rs.{bill['discount_amount']:>8.2f}")
        print(f"{'GST (' + str(int(GST_RATE * 100)) + '%)':<34}Rs.{bill['tax_amount']:>9.2f}")
        print(line)
        print(f"{'GRAND TOTAL':<34}Rs.{bill['grand_total']:>9.2f}")
        print("=" * RECEIPT_WIDTH)
        print("Thank you for dining with us! Visit again.".center(RECEIPT_WIDTH))
        print("=" * RECEIPT_WIDTH + "\n")

    # -----------------------------------------------------------
    # MAIN PROGRAM FLOW
    # -----------------------------------------------------------
    def run(self):
        print("\n" + "#" * RECEIPT_WIDTH)
        print("WELCOME TO THE RESTAURANT BILLING SYSTEM".center(RECEIPT_WIDTH))
        print("#" * RECEIPT_WIDTH)

        customer_name = input("\nEnter Customer Name: ").strip() or "Guest"

        while True:
            self.display_menu()
            self.take_order()

            if self.cart:
                coupon = input(
                    "\nHave a coupon code? (Press Enter to skip): "
                ).strip()
                bill = self.calculate_bill(coupon_code=coupon if coupon else None)
                self.print_receipt(bill, customer_name)

            again = input("Start a new bill? (y/n): ").strip().lower()
            if again != "y":
                print("\nThank you for using the Restaurant Billing System!")
                break
            self.cart = {}   # reset cart for a fresh order


if __name__ == "__main__":
    system = RestaurantBillingSystem()
    system.run()
