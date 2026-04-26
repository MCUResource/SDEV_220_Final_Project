pets = []
owners = []
reservations = []

class Pet:
    def __init__(self, name, pet_type, age, medications, notes):
        self.name = name
        self.pet_type = pet_type
        self.age = age
        self.medications = medications
        self.notes = notes
    
    def __str__(self):
        return f"{self.name} ({self.pet_type}, Age: {self.age})"

class Owner:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
    
    def __str__(self):
        return f"{self.name} (Phone: {self.phone})"

class Reservation:
    def __init__(self, pet_name, owner_name, check_in_date, check_out_date):
        self.pet_name = pet_name
        self.owner_name = owner_name
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.checked_in = False
    
    def __str__(self):
        status = "Checked In" if self.checked_in else "Not Checked In"
        return (f"Pet: {self.pet_name} | Owner: {self.owner_name} | "
                f"{self.check_in_date} to {self.check_out_date} | {status}")

def add_pet():
    name = name_entry.get()
    pet_type = type_entry.get()
    age = age_entry.get()
    medications = meds_entry.get()
    notes = notes_entry.get()

    new_pet = Pet(name, pet_type, age, medications, notes)
    pets.append(new_pet)

    print("Pet added:", new_pet)

    name_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    meds_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)

import tkinter as tk

root = tk.Tk()
root.title("Pet Boarding System")

# Labels and Entry Boxes
tk.Label(root, text="Pet Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Pet Type").pack()
type_entry = tk.Entry(root)
type_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Medications").pack()
meds_entry = tk.Entry(root)
meds_entry.pack()

tk.Label(root, text="Notes").pack()
notes_entry = tk.Entry(root)
notes_entry.pack()

# Button
tk.Button(root, text="Add Pet", command=add_pet).pack()

root.mainloop()
