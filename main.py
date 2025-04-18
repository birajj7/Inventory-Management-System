from datetime import datetime
from colorama import init, Fore, Style
import os

init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("\n" + Fore.CYAN + "=" * 60)
    print(Fore.MAGENTA + Style.BRIGHT + "🧴💄 Welcome to WeCare Beauty & Skincare Store 💅🧼".center(60))
    print(Fore.CYAN + "=" * 60 + "\n")

def get_non_empty_string(prompt):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Input cannot be empty. Please try again.")
        elif value.replace(" ", "").isdigit():
            print("Please enter a valid string (not a number).")
        else:
            return value

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a number greater than 0.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_non_negative_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def read_products(filename='products.txt'):
    if not os.path.exists(filename):
        open(filename, 'w').close()
        return []
    with open(filename, 'r') as file:
        lines = file.readlines()
    products = []
    for line in lines:
        if line.strip() == '':
            continue
        try:
            name, brand, stock, cost_price, country = line.strip().split(',')
            stock = int(stock)
            cost_price = float(cost_price)
            selling_price = cost_price * 2
            products.append({
                'name': name.strip(),
                'brand': brand.strip(),
                'stock': stock,
                'cost_price': cost_price,
                'country': country.strip(),
                'selling_price': selling_price
            })
        except ValueError:
            print(f"Skipping invalid line: {line}")
    return products

def update_products(products, filename='products.txt'):
    with open(filename, 'w') as file:
        for product in products:
            line = f"{product['name']},{product['brand']},{product['stock']},{product['cost_price']},{product['country']}\n"
            file.write(line)

def display_products():
    products = read_products()
    if not products:
        print(Fore.RED + "⚠️  No products available.\n")
        return
    print(Fore.YELLOW + Style.BRIGHT + "\n📦  Available Products:\n")
    print(Fore.GREEN + f"{'Product':<20}{'Brand':<15}{'Stock':<8}{'Price (Rs)':<12}{'Origin'}")
    print(Fore.GREEN + "-" * 65)
    for p in products:
        print(f"{p['name']:<20}{p['brand']:<15}{p['stock']:<8}{p['selling_price']:<12}{p['country']}")
    print(Fore.GREEN + "-" * 65 + "\n")

def sell_products():
    products = read_products()
    customer_name = get_non_empty_string("Enter customer's name: ")
    sold_items = []
    
    while True:
        name = input("Enter product name to sell (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break

        product = next((p for p in products if p['name'].lower() == name.lower()), None)
        if not product:
            print("❌ Product not found.")
            continue

        if product['stock'] == 0:
            print("⚠️ Out of stock.")
            continue

        qty = get_positive_int(f"Enter quantity to sell (Available: {product['stock']}): ")
        if qty > product['stock']:
            print("⚠️ Not enough stock.")
            continue

        product['stock'] -= qty
        sold_items.append({
            'name': product['name'],
            'brand': product['brand'],
            'qty': qty,
            'price': product['selling_price']
        })
    if sold_items:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"SalesInvoice_{now}.txt"
        total = 0

        with open(filename, 'w') as file:
            file.write(f"Customer: {customer_name}\nDate: {datetime.now()}\n\n")
            file.write("Item\tBrand\tQty\tRate\tAmount\n")
            for item in sold_items:
                amt = item['qty'] * item['price']
                total += amt
                file.write(f"{item['name']}\t{item['brand']}\t{item['qty']}\t{item['price']}\t{amt}\n")
            file.write(f"\nTotal Sales Amount: Rs. {total}\n")

        update_products(products)
        print(f"🧾 Sales invoice generated: {filename}")
    else:
        print("🛒 No items sold.")

def restock_products():
    products = read_products()
    vendor_name = get_non_empty_string("Enter vendor/supplier name: ")
    new_items = []
    while True:
        name = input("Enter product name to restock (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        if not name or name.replace(" ", "").isdigit():
            print("Invalid product name. Please enter a proper name.")
            continue
        existing_product = next((p for p in products if p['name'].lower() == name.lower()), None)
        if existing_product:
            qty = get_positive_int(f"Enter quantity to restock for {existing_product['name']}: ")
            price = get_non_negative_float("Enter new cost price (0 to keep existing): ")
            if price > 0:
                existing_product['cost_price'] = price
                existing_product['selling_price'] = price * 2
            existing_product['stock'] += qty
            new_items.append({
                'name': existing_product['name'],
                'brand': existing_product['brand'],
                'qty': qty,
                'cost_price': existing_product['cost_price']
            })
        else:
            print("This is a new product.")
            brand = get_non_empty_string("Enter brand name: ")
            qty = get_positive_int("Enter quantity: ")
            price = get_non_negative_float("Enter cost price per item: ")
            country = get_non_empty_string("Enter country of origin: ")
            new_product = {
                'name': name,
                'brand': brand,
                'stock': qty,
                'cost_price': price,
                'country': country,
                'selling_price': price * 2
            }
            products.append(new_product)
            new_items.append({
                'name': name,
                'brand': brand,
                'qty': qty,
                'cost_price': price
            })
    if new_items:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"RestockInvoice_{now}.txt"
        total = 0
        with open(filename, 'w') as file:
            file.write(f"Supplier: {vendor_name}\nDate: {datetime.now()}\n\n")
            file.write("Item\tBrand\tQty\tRate\tAmount\n")
            for item in new_items:
                amt = item['qty'] * item['cost_price']
                total += amt
                file.write(f"{item['name']}\t{item['brand']}\t{item['qty']}\t{item['cost_price']}\t{amt}\n")
            file.write(f"\nTotal Purchase Amount: Rs. {total}\n")
        update_products(products)
        print(f"Restock invoice generated: {filename}")

def main():
    while True:
        clear_screen()
        banner()
        print(Fore.BLUE + Style.BRIGHT + "🧭 Main Menu:")
        print(Fore.CYAN + "1️⃣  Show Available Products")
        print("2️⃣  Sell Products")
        print("3️⃣  Restock Products")
        print("4️⃣  Exit")
        choice = input(Fore.YELLOW + "\n👉 Enter your choice (1-4): ").strip()
        if choice == '1':
            clear_screen()
            banner()
            display_products()
            input(Fore.MAGENTA + "🔁 Press Enter to return to the main menu...")
        elif choice == '2':
            clear_screen()
            banner()
            sell_products()
            input(Fore.MAGENTA + "🧾 Press Enter to return to the main menu...")
        elif choice == '3':
            clear_screen()
            banner()
            restock_products()
            input(Fore.MAGENTA + "📦 Press Enter to return to the main menu...")
        elif choice == '4':
            print(Fore.GREEN + "\n👋 Thank you for using WeCare System. Stay beautiful! 💖\n")
            break
        else:
            print(Fore.RED + "\n❌ Invalid choice. Please try again (1-4).")
            input(Fore.YELLOW + "🔁 Press Enter to continue...")

if __name__ == "__main__":
    main()
