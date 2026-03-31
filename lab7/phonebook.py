import psycopg2
import csv

conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",      
    password="1234",      
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Added!")

def show_contacts():
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

def search_contact():
    keyword = input("Search name: ")
    cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", ('%' + keyword + '%',))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching contacts.")

def update_contact():
    name = input("Name to update: ")
    new_phone = input("New phone: ")
    cur.execute("UPDATE contacts SET phone = %s WHERE name = %s", (new_phone, name))
    conn.commit()
    print("Updated!")

def delete_contact():
    name = input("Name to delete: ")
    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
    conn.commit()
    print("Deleted!")

def import_from_csv():
    try:
        with open("contacts.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row["name"], row["phone"]))
        conn.commit()
        print("CSV imported!")
    except FileNotFoundError:
        print("contacts.csv not found. Please place it in the same folder as this script.")


while True:
    print("\n1.Add 2.Show 3.Search 4.Update 5.Delete 6.Import CSV 7.Exit")
    choice = input("Choose: ")
    if choice == "1":
        add_contact()
    elif choice == "2":
        show_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        update_contact()
    elif choice == "5":
        delete_contact()
    elif choice == "6":
        import_from_csv()
    elif choice == "7":
        break
    else:
        print("Invalid choice. Try again.")

cur.close()
conn.close()