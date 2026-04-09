import csv
import random

# Configuration
NUM_ROWS = 150
OUTPUT_FILE = "sample_data.csv"

first_names = ["Thabo", "Lerato", "Sipho", "Naledi", "Johan", "Pieter", "Amina", "Zanele", "Kagiso", "Fatima", "David", "Sarah"]
last_names = ["Ndlovu", "Botha", "Dlamini", "Smith", "Nkosi", "VanDerMerwe", "Patel", "Molefe", "Mkhize", "Naidoo", "Cohen", "Jones"]
domains = ["gmail.com", "company.za", "webmail.co.za", "startup.io"]

print(f"Generating {NUM_ROWS} rows of messy data...")

with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Adding phone_number so your Privacy Agent actually finds it this time!
    writer.writerow(["user_id", "sa_id", "email", "phone_number", "age", "purchase_amount"])

    for i in range(1, NUM_ROWS + 1):
        user_id = f"U-{1000 + i}"
        
        # Generate fake 13-digit SA ID (YYMMDD + 4 digits + 08/18 + 1)
        yy = str(random.randint(50, 99))
        mm = str(random.randint(1, 12)).zfill(2)
        dd = str(random.randint(1, 28)).zfill(2)
        seq = str(random.randint(0, 9999)).zfill(4)
        cz = str(random.choice([0, 1])) + "8" + str(random.randint(0, 9))
        sa_id = f"{yy}{mm}{dd}{seq}{cz}"
        
        # 15% chance to be missing an email
        if random.random() > 0.15:
            fname = random.choice(first_names).lower()
            lname = random.choice(last_names).lower()
            email = f"{fname}.{lname}{random.randint(1,99)}@{random.choice(domains)}"
        else:
            email = ""

        # Fake South African Phone Number
        phone = f"0{random.randint(6,8)}{random.randint(1,9)} {random.randint(100,999)} {random.randint(1000,9999)}"
        
        # 10% chance to be missing age
        age = random.randint(18, 65) if random.random() > 0.10 else ""
        
        # 20% chance to be missing purchase amount
        purchase = round(random.uniform(15.0, 999.99), 2) if random.random() > 0.20 else ""
        
        writer.writerow([user_id, sa_id, email, phone, age, purchase])

print(f"✅ Success! Overwritten {OUTPUT_FILE} with new messy data.")