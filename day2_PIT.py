import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

FILE_NAME = "attendance.txt"


def validate_student_id(student_id):
    return student_id.isdigit() and len(student_id) == 10


def load_records():
    try:
        with open(FILE_NAME, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def time_in():
    student_id = entry_id.get().strip()
    name = entry_name.get().strip()

    if not student_id or not name:
        messagebox.showerror("Error", "All fields are required")
        return

    if not validate_student_id(student_id):
        messagebox.showerror("Error", "ID must be exactly 10 digits")
        return

    time_now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    with open(FILE_NAME, "a") as file:
        file.write(f"{student_id},{name},TIME IN,{time_now}\n")

    messagebox.showinfo("Success", "Time In recorded successfully")
    update_dashboard()


def time_out():
    student_id = entry_id.get().strip()
    name = entry_name.get().strip()

    if not student_id or not name:
        messagebox.showerror("Error", "All fields are required")
        return

    if not validate_student_id(student_id):
        messagebox.showerror("Error", "ID must be exactly 10 digits")
        return

    time_now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    with open(FILE_NAME, "a") as file:
        file.write(f"{student_id},{name},TIME OUT,{time_now}\n")

    messagebox.showinfo("Success", "Time Out recorded successfully")
    update_dashboard()


def update_dashboard():
    records = load_records()

    total = len(records)
    present = set()
    late = 0

    for r in records:
        try:
            sid, name, status, time_str = r.strip().split(",")

            present.add(sid)

            t = datetime.strptime(time_str, "%Y-%m-%d %I:%M %p")

            if status == "TIME IN" and t.hour >= 8:
                late += 1

        except:
            continue

    label_total.config(text=f"Total Records: {total}")
    label_present.config(text=f"Present Students: {len(present)}")
    label_late.config(text=f"Late Students: {late}")


def view_records():
    records = load_records()

    win = tk.Toplevel(root)
    win.title("Attendance Records")
    win.geometry("900x500")
    win.configure(bg="#e6f2ff")

    tk.Label(win, text="TIME IN RECORDS", font=("Arial", 14, "bold"), bg="#e6f2ff", fg="green").pack(pady=5)

    tree_in = ttk.Treeview(win, columns=("ID", "Name", "Time"), show="headings", height=8)
    tree_in.heading("ID", text="Student ID")
    tree_in.heading("Name", text="Name")
    tree_in.heading("Time", text="Time In")

    tree_in.column("ID", width=150)
    tree_in.column("Name", width=200)
    tree_in.column("Time", width=250)

    tree_in.pack(pady=5)

    tk.Label(win, text="TIME OUT RECORDS", font=("Arial", 14, "bold"), bg="#e6f2ff", fg="red").pack(pady=10)

    tree_out = ttk.Treeview(win, columns=("ID", "Name", "Time"), show="headings", height=8)
    tree_out.heading("ID", text="Student ID")
    tree_out.heading("Name", text="Name")
    tree_out.heading("Time", text="Time Out")

    tree_out.column("ID", width=150)
    tree_out.column("Name", width=200)
    tree_out.column("Time", width=250)

    tree_out.pack(pady=5)

    for r in records:
        try:
            sid, name, status, time_str = r.strip().split(",")

            if status == "TIME IN":
                tree_in.insert("", tk.END, values=(sid, name, time_str))

            elif status == "TIME OUT":
                tree_out.insert("", tk.END, values=(sid, name, time_str))

        except:
            continue


root = tk.Tk()
root.title("USTP Attendance System")
root.state("zoomed")
root.configure(bg="#d9f2ff")

tk.Label(root, text="USTP ATTENDANCE SYSTEM", font=("Arial", 26, "bold"), bg="#d9f2ff", fg="#003366").pack(pady=15)

frame = tk.Frame(root, bg="#d9f2ff")
frame.pack(pady=10)

tk.Label(frame, text="Student ID:", bg="#d9f2ff", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(frame, font=("Arial", 12), width=25)
entry_id.grid(row=0, column=1)

tk.Label(frame, text="Name:", bg="#d9f2ff", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame, font=("Arial", 12), width=25)
entry_name.grid(row=1, column=1)

# BUTTONS
btn_frame = tk.Frame(root, bg="#d9f2ff")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Time In", width=15, bg="#4CAF50", fg="white", font=("Arial", 11), command=time_in).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Time Out", width=15, bg="#f44336", fg="white", font=("Arial", 11), command=time_out).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="View Table", width=15, bg="#2196F3", fg="white", font=("Arial", 11), command=view_records).grid(row=0, column=2, padx=5)

# DASHBOARD
dash = tk.Frame(root, bg="#d9f2ff")
dash.pack(pady=30)

label_total = tk.Label(dash, text="Total Records: 0", font=("Arial", 14, "bold"), bg="#d9f2ff")
label_total.grid(row=0, column=0, padx=30)

label_present = tk.Label(dash, text="Present Students: 0", font=("Arial", 14, "bold"), bg="#d9f2ff")
label_present.grid(row=0, column=1, padx=30)

label_late = tk.Label(dash, text="Late Students: 0", font=("Arial", 14, "bold"), bg="#d9f2ff")
label_late.grid(row=0, column=2, padx=30)

update_dashboard()

root.mainloop()