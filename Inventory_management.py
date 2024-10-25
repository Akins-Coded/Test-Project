import mysql.connector
import csv

# Connect to the database
def db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Akinscoded",
        database="Inventory"
    )

# Function to manage the inventory
class InventoryManagement:
    # Add a product
    def add_product(self, product_name, category, stock_quantity, price):
        connection = db()
        cursor = connection.cursor()
        sql = "INSERT INTO products (product_name, category, stock_quantity, price) VALUES (%s, %s, %s, %s)"
        val = (product_name, category, stock_quantity, price)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Product '{product_name}' added successfully!")

    # View all products
    def view_products(self):
        connection = db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        for product in products:  # Changed products() to products
            print(product)
        cursor.close()
        connection.close()

    # Update product details
    def update_product(self, product_id, product_name=None, category=None, price=None, stock_quantity=None):
        connection = db()
        cursor = connection.cursor()

        if product_name:
            cursor.execute("UPDATE products SET product_name = %s WHERE product_id = %s", (product_name, product_id))
        if category:
            cursor.execute("UPDATE products SET category = %s WHERE product_id = %s", (category, product_id))
        if price is not None:
            cursor.execute("UPDATE products SET price = %s WHERE product_id = %s", (price, product_id))
        if stock_quantity is not None:
            cursor.execute("UPDATE products SET stock_quantity = %s WHERE product_id = %s", (stock_quantity, product_id))

        connection.commit()
        print("Product updated successfully!")
        cursor.close()
        connection.close()

    # Delete a product
    def delete_product(self, product_id):
        connection = db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        connection.commit()
        cursor.close()
        connection.close()
        print("Product deleted successfully")

    # Low-Stock Alert: Generate alerts for products with stock below a specified threshold
    def low_stock(self, min_threshold=5):  # Added self as parameter
        connection = db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE stock_quantity < %s", (min_threshold,))
        low_stock_products = cursor.fetchall()
        if low_stock_products:
            print("Low Stock Alert For:")
            for product in low_stock_products:
                print(product)
        else:
            print("No low stock products.")
        cursor.close()
        connection.close()

    # Search products by name or category
    def search_products(self, item):
        connection = db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products WHERE product_name LIKE %s OR category LIKE %s", (f"%{item}%", f"%{item}%"))
        products = cursor.fetchall()
        for product in products:
            print(product)
        cursor.close()
        connection.close()

    # Sort products by price or stock quantity
    def sort_products(self, order_by):
        connection = db()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM products ORDER BY {order_by}")  # Note: Be cautious with SQL injection here
        products = cursor.fetchall()
        for product in products:
            print(product)
        cursor.close()
        connection.close()

    # Export to CSV
    def csv_file_export(self, filename="Inventory_report.csv"):
        connection = db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Product Id', 'Name', 'Category', 'Stock Quantity', 'Price'])
            writer.writerows(cursor.fetchall())
        cursor.close()
        connection.close()
        print(f"Data exported to {filename} successfully!")

if __name__ == "__main__":
    inventory = InventoryManagement()

    while True:
        print("\n Coded Ent Inventory Management System")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Low Stock Alert")
        print("6. Search Products")
        print("7. Sort Products")
        print("8. Export Database to CSV")
        print("9. Exit")

        choice = input("Select an Option: ")

        if choice == "1":
            product_name = input("Enter Product Name: ")
            category = input("Enter Category: ")
            stock_quantity = int(input("Enter Stock Quantity: "))
            price = float(input("Enter Price: "))
            inventory.add_product(product_name, category, stock_quantity, price)

        elif choice == "2":
            inventory.view_products()

        elif choice == "3":
            product_id = int(input("Enter Product ID to update: "))
            product_name = input("Enter new name (leave blank to skip): ")
            category = input("Enter new category (leave blank to skip): ")
            price = input("Enter new price (leave blank to skip): ")
            stock_quantity = input("Enter new stock quantity (leave blank to skip): ")
            inventory.update_product(
                product_id,
                product_name if product_name else None,
                category if category else None,
                float(price) if price else None,
                int(stock_quantity) if stock_quantity else None
            )
        elif choice == "4":
            product_id = int(input("Enter the product ID to delete: "))
            inventory.delete_product(product_id)

        elif choice == "5":
            inventory.low_stock()

        elif choice == "6":
            item = input("Enter the name of what you're searching for: ")
            inventory.search_products(item)

        elif choice == "7":
            order_by = input("Sort by Price/Quantity? : ")
            inventory.sort_products(order_by)

        elif choice == "8":
            inventory.csv_file_export()

        elif choice == "9":
            print("Thanks for your time...")
            break

        else:
            print("Invalid Choice. Please try again!")
