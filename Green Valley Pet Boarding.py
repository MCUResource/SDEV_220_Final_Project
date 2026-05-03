import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

root = tk.Tk()
root.title("Pet Boarding System")
root.geometry("500x700")

main_canvas = tk.Canvas(root)
main_canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollbar.pack(side="right", fill="y")

scrollable_frame = tk.Frame(main_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda event: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def resize_scrollable_frame(event):
    main_canvas.itemconfig(canvas_window, width=event.width)

main_canvas.bind("<Configure>", resize_scrollable_frame)
main_canvas.configure(yscrollcommand=scrollbar.set)

pets = []
owners = []
reservations = []
reservation_lookup = {}

selected_owner = tk.StringVar(root)
selected_pet = tk.StringVar(root)
selected_reservation = tk.StringVar(root)

class Pet:
    def __init__(self, name, pet_type, age, medications, notes, owner):
        self.name = name
        self.pet_type = pet_type
        self.age = age
        self.medications = medications
        self.notes = notes
        self.owner = owner
    
    def __str__(self):
        return f"{self.name} ({self.pet_type}, Age: {self.age}, Owner: {self.owner.name})"

class Owner:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.pets = []
    
    def add_pet(self, pet):
        self.pets.append(pet)
    
    def __str__(self):
        return f"{self.name} (Phone: {self.phone}, Pets: {len(self.pets)})"

class Reservation:
    def __init__(self, pet, check_in_date, check_out_date):
        self.pet = pet
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.checked_in = False
        self.checked_out = False
    
    def __str__(self):
        if self.checked_out:
            status = "Checked Out"
        elif self.checked_in:
            status = "Checked In"
        else:
            status = "Not Checked In"
        return (f"Pet: {self.pet.name} | Owner: {self.pet.owner.name} | "
                f"{self.check_in_date} to {self.check_out_date} | {status}")

def find_owner_by_name(name):
    for owner in owners:
        if owner.name == name:
            return owner
    return None

def update_pet_dropdown(*args):
    selected_pet.set("")
    pet_dropdown["menu"].delete(0, "end")

    owner = find_owner_by_name(selected_owner.get())

    if owner is None:
        return
    
    for pet in owner.pets:
        pet_dropdown["menu"].add_command(
            label=pet.name,
            command=tk._setit(selected_pet, pet.name)
        )

def find_pet_by_name(name):
    owner = find_owner_by_name(selected_owner.get())

    if owner is None:
        return None
    
    for pet in owner.pets:
        if pet.name == name:
            return pet
        
    return None

def add_owner():
    owner_error_label.config(text="")

    name = owner_name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name == "" or phone == "" or email == "":
        owner_error_label.config(text="Please fill in all owner fields.")
        return

    new_owner = Owner(name, phone, email)
    owners.append(new_owner)

    selected_owner.set(name)
    owner_dropdown["menu"].add_command(
        label=name,
        command=tk._setit(selected_owner, name)
    )

    print("Owner added:", new_owner)

    owner_name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    pet_frame.pack(pady=10)

def add_pet():
    pet_error_label.config(text="")

    owner = find_owner_by_name(selected_owner.get())

    if owner is None:
        pet_error_label.config(text="Please add or select an owner first.")
        return
    
    name = name_entry.get()
    pet_type = type_entry.get()
    age = age_entry.get()
    medications = meds_entry.get()
    notes = notes_entry.get()

    if name == "" or pet_type == "" or age == "":
        pet_error_label.config(text="Please fill in all required pet fields.")
        return

    new_pet = Pet(name, pet_type, age, medications, notes, owner)
    pets.append(new_pet)
    owner.add_pet(new_pet)

    selected_pet.set(name)
    update_pet_dropdown()
    selected_pet.set(name)

    print("Pet added:", new_pet)

    name_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    meds_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)

    reservation_frame.pack(pady=10)

def add_reservation():
    reservation_error_label.config(text="")

    pet = find_pet_by_name(selected_pet.get())

    if pet is None:
        reservation_error_label.config(text="Please add or select a pet first.")
        return
    
    check_in_date = check_in_entry.get()
    check_out_date = check_out_entry.get()

    if check_in_date == "" or check_out_date == "":
        reservation_error_label.config(text="Please enter both check-in and check-out dates.")
        return

    new_reservation = Reservation(pet, check_in_date, check_out_date)
    reservations.append(new_reservation)

    update_reservation_dropdown()
    selected_reservation.set("")

    print("Reservation added:", new_reservation)

    check_in_entry.delete(0, tk.END)
    check_out_entry.delete(0, tk.END)

def check_in_reservation():
    selected_label = selected_reservation.get()

    if selected_label == "":
        reservation_error_label.config(text="Please select a reservation to check in.")
        return
    
    index = reservation_lookup[selected_label]
    reservation = reservations[index]

    confirm = messagebox.askyesno(
        "Confirm Check In",
        f"Check in {reservation.pet.name} "
        f"({reservation.check_in_date} to {reservation.check_out_date})?"
    )

    if not confirm:
        return
    
    reservation.checked_in = True

    print("Reservation checked in:", reservation)

    update_reservation_dropdown()
    selected_reservation.set("")

def update_reservation_dropdown(*args):
    selected_reservation.set("")
    reservation_dropdown["menu"].delete(0, "end")
    reservation_lookup.clear()

    owner = find_owner_by_name(selected_owner.get())

    if owner is None:
        return
    
    for index, reservation in enumerate(reservations):
        if reservation.pet.owner == owner:
            if reservation.checked_out:
                status = "Checked Out"
            elif reservation.checked_in:
                status = "Checked In"
            else:
                status = "Not Checked In"
            label = f"{reservation.pet.name}: {reservation.check_in_date} to {reservation.check_out_date} | {status}"

            reservation_lookup[label] = index

            reservation_dropdown["menu"].add_command(
                label=label,
                command=tk._setit(selected_reservation, label)
            )

def delete_reservation():
    selected_label = selected_reservation.get()

    if selected_label == "":
        reservation_error_label.config(text="Please select a reservation to delete.")
        return
    
    index = reservation_lookup[selected_label]
    reservation = reservations[index]
    
    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete the reservation for {reservation.pet.name} "
        f"({reservation.check_in_date} to {reservation.check_out_date})?"
    )

    if not confirm:
        return
    
    removed_reservation = reservations.pop(index)

    reservation_error_label.config(
        text=f"Deleted reservation for {removed_reservation.pet.name}."
    )
    
    update_reservation_dropdown()
    selected_reservation.set("")

    print("Reservation deleted:", removed_reservation)

def check_out_reservation():
    selected_label = selected_reservation.get()

    if selected_label == "":
        reservation_error_label.config(text="Please select a reservation to check out.")
        return
    
    index = reservation_lookup[selected_label]
    reservation = reservations[index]

    if not reservation.checked_in:
        reservation_error_label.config(text="Reservation must be checked in before checking out.")
        return
    
    confirm = messagebox.askyesno(
        "Confirm Check Out",
        f"Check out {reservation.pet.name} "
        f"({reservation.check_in_date} to {reservation.check_out_date})?"
    )

    if not confirm:
        return
    
    reservation.checked_out = True

    print("Reservation checked out:", reservation)

    update_reservation_dropdown()
    selected_reservation.set("")

def open_calendar(entry_box):
    calendar_window = tk.Toplevel(root)
    calendar_window.title("Select Date")

    cal = Calendar(calendar_window, selectmode="day", date_pattern="mm/dd/yyyy")
    cal.pack(pady=10)

    def select_date():
        entry_box.delete(0, tk.END)
        entry_box.insert(0, cal.get_date())
        calendar_window.destroy()
    
    tk.Button(calendar_window, text="Select Date", command=select_date).pack(pady=10)

# Labels and Entry Boxes

# Owner
owner_frame = tk.Frame(scrollable_frame)
owner_frame.pack(pady=10)

owner_error_label = tk.Label(owner_frame, text="", fg="red")
owner_error_label.pack()

tk.Label(owner_frame, text="Add or Select Owner").pack()

tk.Label(owner_frame, text="Owner Name").pack()
owner_name_entry = tk.Entry(owner_frame)
owner_name_entry.pack()

tk.Label(owner_frame, text="Phone").pack()
phone_entry = tk.Entry(owner_frame)
phone_entry.pack()

tk.Label(owner_frame, text="Email").pack()
email_entry = tk.Entry(owner_frame)
email_entry.pack()

tk.Button(owner_frame, text="Add Owner", command=add_owner).pack(pady=5)

tk.Label(owner_frame, text="Select Existing Owner").pack()
owner_dropdown = tk.OptionMenu(owner_frame, selected_owner, "")
owner_dropdown.pack()

# Pet

pet_frame = tk.Frame(scrollable_frame)

pet_error_label = tk.Label(pet_frame, text="", fg="red")
pet_error_label.pack()

tk.Label(pet_frame, text="Add or Select Pet").pack()

tk.Label(pet_frame, text="Pet Name").pack()
name_entry = tk.Entry(pet_frame)
name_entry.pack()

tk.Label(pet_frame, text="Pet Type").pack()
type_entry = tk.Entry(pet_frame)
type_entry.pack()

tk.Label(pet_frame, text="Age").pack()
age_entry = tk.Entry(pet_frame)
age_entry.pack()

tk.Label(pet_frame, text="Medications").pack()
meds_entry = tk.Entry(pet_frame)
meds_entry.pack()

tk.Label(pet_frame, text="Notes").pack()
notes_entry = tk.Entry(pet_frame)
notes_entry.pack()

tk.Button(pet_frame, text="Add Pet", command=add_pet).pack(pady=5)

tk.Label(pet_frame, text="Select Existing Pet").pack()
pet_dropdown = tk.OptionMenu(pet_frame, selected_pet, "")
pet_dropdown.pack()

selected_owner.trace_add("write", update_pet_dropdown)

# Reservation

reservation_frame = tk.Frame(scrollable_frame)

reservation_error_label = tk.Label(reservation_frame, text="", fg="red")
reservation_error_label.pack()

tk.Label(reservation_frame, text="Add Reservation").pack()

tk.Label(reservation_frame, text="Check-In Date").pack()
check_in_entry = tk.Entry(reservation_frame)
check_in_entry.pack()
check_in_entry.bind("<Button-1>", lambda event: open_calendar(check_in_entry))

tk.Label(reservation_frame, text="Check-Out Date").pack()
check_out_entry = tk.Entry(reservation_frame)
check_out_entry.pack()
check_out_entry.bind("<Button-1>", lambda event: open_calendar(check_out_entry))

tk.Button(reservation_frame, text="Add Reservation", command=add_reservation).pack(pady=5)

tk.Label(reservation_frame, text="Select Reservation").pack()
reservation_dropdown = tk.OptionMenu(reservation_frame, selected_reservation, "")
reservation_dropdown.pack()

selected_owner.trace_add("write", update_reservation_dropdown)

tk.Button(reservation_frame, text="Check In Selected Reservation", command=check_in_reservation).pack(pady=5)

tk.Button(reservation_frame, text="Check Out Selected Reservation", command=check_out_reservation).pack(pady=5)

tk.Button(reservation_frame, text="Delete Selected Reservation", command=delete_reservation).pack(pady=5)

root.mainloop()
