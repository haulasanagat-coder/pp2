import psycopg2
import json
import csv
from datetime import datetime
from connect import get_db_connection

# Helper Functions
def print_contacts(contacts):
    """Pretty print contact list"""
    if not contacts:
        print("No contacts found.")
        return
    
    for c in contacts:
        print(f"\nID: {c[0]}")
        print(f"Name: {c[1]}")
        print(f"Email: {c[2] or 'N/A'}")
        print(f"Birthday: {c[3] or 'N/A'}")
        print(f"Group: {c[4] or 'N/A'}")
        print(f"Phones: {c[5] or 'N/A'}")

def paginated_view(query_results, page_size=2):
    """Paginate contact results (next/prev/quit)"""
    if not query_results:
        print("\n❌ No contacts found.")
        return

    total = len(query_results)
    pages = [query_results[i:i+page_size] for i in range(0, total, page_size)]
    current = 0

    while True:
        print(f"\n=== Page {current+1}/{len(pages)} ===")
        print_contacts(pages[current])

        cmd = input("\nNavigate: [n]ext | [p]rev | [q]uit: ").lower().strip()
        if cmd == 'n' and current < len(pages)-1:
            current +=1
        elif cmd == 'p' and current >0:
            current -=1
        elif cmd == 'q':
            break
        else:
            print("Invalid command")

# 3.1 Core Features
def add_contact():
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")

    # Validate birthday format
    birthday = None
    while True:
        birthday_input = input("Birthday (YYYY-MM-DD): ")
        if not birthday_input:
            break
        try:
            datetime.strptime(birthday_input, "%Y-%m-%d")
            birthday = birthday_input
            break
        except ValueError:
            print("❌ Invalid format! Use YYYY-MM-DD (e.g., 2009-08-29)")

    group = input("Group (Family/Work/Friend/Other): ")
    phone = input("Phone: ")
    p_type = input("Phone type (home/work/mobile): ")

    # Get or create group
    cur.execute("SELECT id FROM groups WHERE name ILIKE %s", (group,))
    g_id = cur.fetchone()
    if not g_id:
        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group,))
        g_id = cur.fetchone()[0]
    else:
        g_id = g_id[0]

    # Insert contact
    cur.execute("""
        INSERT INTO contacts (name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (name, email, birthday, g_id))
    c_id = cur.fetchone()[0]

    # Insert phone
    cur.execute("""
        INSERT INTO phones (contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (c_id, phone, p_type))

    conn.commit()
    print("✅ Contact added!")
    cur.close()
    conn.close()

# 3.2 Advanced Search & Filter
def filter_by_group():
    group = input("Enter group name: ")
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               STRING_AGG(ph.type || ': ' || ph.phone, ', ')
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones ph ON c.id = ph.contact_id
        WHERE g.name ILIKE %s
        GROUP BY c.id, g.name
    """, (group,))
    results = cur.fetchall()
    paginated_view(results)
    cur.close()
    conn.close()

def search_by_email():
    query = input("Search email (partial): ")
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               STRING_AGG(ph.type || ': ' || ph.phone, ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones ph ON c.id = ph.contact_id
        WHERE c.email ILIKE %s
        GROUP BY c.id, g.name
    """, (f'%{query}%',))
    results = cur.fetchall()
    paginated_view(results)
    cur.close()
    conn.close()

def sort_contacts():
    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date Added")
    choice = input("Choice: ")

    sort = {"1":"c.name", "2":"c.birthday", "3":"c.created_at"}.get(choice, "c.name")
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.name, c.email, c.birthday, g.name,
               STRING_AGG(ph.type || ': ' || ph.phone, ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones ph ON c.id = ph.contact_id
        GROUP BY c.id, g.name
        ORDER BY {sort}
    """)
    results = cur.fetchall()
    paginated_view(results)
    cur.close()
    conn.close()

# 3.3 Import / Export
def export_json():
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name as group,
               json_agg(json_build_object('type', ph.type, 'number', ph.phone)) as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones ph ON c.id = ph.contact_id
        GROUP BY c.id, g.name
    """)
    contacts = []
    for row in cur.fetchall():
        contacts.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "birthday": str(row[3]) if row[3] else None,
            "group": row[4],
            "phones": row[5] if row[5] != [None] else []
        })
    with open("contacts.json", "w") as f:
        json.dump(contacts, f, indent=2)
    print("✅ Exported to contacts.json")
    cur.close()
    conn.close()

def import_json():
    try:
        with open("contacts.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ contacts.json not found!")
        return
    
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()

    for item in data:
        name = item["name"]
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"Contact {name} exists! [s]kip/[o]verwrite: ").lower()
            if choice == 's':
                continue
            elif choice == 'o':
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
            else:
                continue

        # Group
        g_name = item.get("group", "Other")
        cur.execute("SELECT id FROM groups WHERE name = %s", (g_name,))
        g_id = cur.fetchone()
        if not g_id:
            cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (g_name,))
            g_id = cur.fetchone()[0]
        else:
            g_id = g_id[0]

        # Contact
        cur.execute("""
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (name, item.get("email"), item.get("birthday"), g_id))
        c_id = cur.fetchone()[0]

        # Phones
        for p in item.get("phones", []):
            if p and p.get("number"):
                cur.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (c_id, p["number"], p.get("type", "mobile")))

    conn.commit()
    print("✅ JSON import complete!")
    cur.close()
    conn.close()

def import_csv():
    try:
        with open("contacts.csv", "r") as f:
            reader = csv.DictReader(f)
            data = list(reader)
    except FileNotFoundError:
        print("❌ contacts.csv not found!")
        return

    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()

    for row in data:
        name = row["name"]
        email = row.get("email")
        birthday = row.get("birthday")
        group = row.get("group", "Other")
        phone = row.get("phone")
        p_type = row.get("phone_type", "mobile")

        # Group
        cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
        g_id = cur.fetchone()
        if not g_id:
            cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group,))
            g_id = cur.fetchone()[0]
        else:
            g_id = g_id[0]

        # Contact
        cur.execute("""
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id
        """, (name, email, birthday, g_id))
        c_id = cur.fetchone()
        if not c_id:
            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            c_id = cur.fetchone()[0]
        else:
            c_id = c_id[0]

        # Phone
        if phone:
            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (c_id, phone, p_type))

    conn.commit()
    print("✅ CSV imported!")
    cur.close()
    conn.close()

# 3.4 Call Stored Procedures
def call_add_phone():
    name = input("Contact name: ")
    phone = input("Phone number: ")
    p_type = input("Type (home/work/mobile): ")
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, p_type))
        conn.commit()
        print("✅ Phone added!")
    except Exception as e:
        print(f"❌ Error: {e}")
    cur.close()
    conn.close()

def call_move_group():
    name = input("Contact name: ")
    group = input("New group: ")
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("✅ Group updated!")
    except Exception as e:
        print(f"❌ Error: {e}")
    cur.close()
    conn.close()

def call_search():
    q = input("Search query: ")
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    results = cur.fetchall()
    paginated_view(results)
    cur.close()
    conn.close()

# Main Menu
def main():
    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Add contact")
        print("2. Filter by group")
        print("3. Search by email")
        print("4. Sort contacts")
        print("5. Export JSON")
        print("6. Import JSON")
        print("7. Import CSV")
        print("8. Add phone (procedure)")
        print("9. Move to group (procedure)")
        print("10. Advanced search (function)")
        print("0. Exit")
        choice = input("Choose: ")

        if choice == "1": add_contact()
        elif choice == "2": filter_by_group()
        elif choice == "3": search_by_email()
        elif choice == "4": sort_contacts()
        elif choice == "5": export_json()
        elif choice == "6": import_json()
        elif choice == "7": import_csv()
        elif choice == "8": call_add_phone()
        elif choice == "9": call_move_group()
        elif choice == "10": call_search()
        elif choice == "0": break
        else: print("Invalid choice")

if __name__ == "__main__":
    main()