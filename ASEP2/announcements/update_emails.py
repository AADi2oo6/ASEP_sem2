import csv
from django.db.models import Q
from login.models import login  # adjust this import based on your app structure

def update_emails_from_csv(csv_path):
    # Step 1: Load CSV to a dictionary
    csv_data = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name'].strip().lower()
            email = row['email'].strip()
            csv_data[name] = email

    # Step 2: Go through all login entries
    updates = 0
    all_students = login.objects.all()
    for student in all_students:
        db_name = student.Name.strip().lower()
        if db_name in csv_data:
            new_email = csv_data[db_name]
            if student.userName != new_email:
                print(f"Updating: {student.Name} | {student.userName} → {new_email}")
                student.userName = new_email
                student.save()
                updates += 1

    print(f"\n✅ Done. {updates} email(s) updated.")

# Example usage 
update_emails_from_csv('email.csv')
