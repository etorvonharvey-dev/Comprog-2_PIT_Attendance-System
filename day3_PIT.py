import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

FILE_NAME = "attendance.txt"

def validate_id(student_id):
    return student_id.isdigit() and len(student_id) == 10


def load_records():
    try:
        with open(FILE_NAME, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)


def already_timed_in(student_id):
    today = datetime.now().strftime("%Y-%m-%d")

    for record in load_records():
        try:
            sid, name, status, time_str = record.strip().split(",")

            record_date = datetime.strptime(
                time_str,
                "%Y-%m-%d %I:%M %p"
            ).strftime("%Y-%m-%d")

            if sid == student_id and status == "TIME IN" and record_date == today:
                return True

        except:
            continue

    return False


def update_dashboard():
    records = load_records()

    total = len(records)
    students = set()
    late = 0

    for record in records:
        try:
            sid, name, status, time_str = record.strip().split(",")

            students.add(sid)

            t = datetime.strptime(time_str, "%Y-%m-%d %I:%M %p")

            if status == "TIME IN" and t.hour >= 8:
                late += 1

        except:
            continue

    total_label.config(text=str(total))
    present_label.config(text=str(len(students)))
    late_label.config(text=str(late))


def refresh_table():
    for item in tree.get_children():
        tree.delete(item)

    for record in load_records():
        try:
            sid, name, status, time_str = record.strip().split(",")

            tree.insert(
                "",
                tk.END,
                values=(sid, name, status, time_str)
            )

        except:
            continue


def save_attendance(status):
    student_id = entry_id.get().strip()
    name = entry_name.get().strip()

    if not student_id or not name:
        messagebox.showerror("Error", "All fields are required")
        return

    if not validate_id(student_id):
        messagebox.showerror("Error", "ID must be exactly 10 digits")
        return

    if status == "TIME IN" and already_timed_in(student_id):
        messagebox.showwarning(
            "Duplicate Entry",
            "Student already timed in today"
        )
        return

    time_now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    try:
        with open(FILE_NAME, "a") as file:
            file.write(
                f"{student_id},{name},{status},{time_now}\n"
            )

        messagebox.showinfo(
            "Success",
            f"{status} recorded successfully"
        )

        clear_fields()
        refresh_table()
        update_dashboard()

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("USTP Attendance System")
root.state("zoomed")
root.configure(bg="#f7dede")

main = tk.Frame(root, bg="#fff5f5")
main.pack(fill="both", expand=True, padx=20, pady=20)

header = tk.Frame(main, bg="white", height=70)
header.pack(fill="x")

tk.Label(
    header,
    text="USTP ATTENDANCE SYSTEM",
    font=("Segoe UI", 20, "bold"),
    bg="white",
    fg="#990000"
).pack(side="left", padx=20, pady=15)

tk.Label(
    header,
    text="Admin",
    font=("Segoe UI", 10),
    bg="white"
).pack(side="right", padx=20)

dashboard = tk.Frame(main, bg="#fff5f5")
dashboard.pack(pady=20)

def create_card(parent, title):
    frame = tk.Frame(
        parent,
        bg="white",
        width=220,
        height=100,
        bd=1,
        relief="solid"
    )
    frame.pack_propagate(False)

    number = tk.Label(
        frame,
        text="0",
        font=("Segoe UI", 22, "bold"),
        bg="white"
    )
    number.pack(pady=10)

    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 10),
        bg="white"
    ).pack()

    return frame, number


card1, total_label = create_card(dashboard, "Total Records")
card1.grid(row=0, column=0, padx=10)

card2, present_label = create_card(dashboard, "Present Students")
card2.grid(row=0, column=1, padx=10)

card3, late_label = create_card(dashboard, "Late Students")
card3.grid(row=0, column=2, padx=10)

form = tk.LabelFrame(
    main,
    text="Attendance Form",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    padx=20,
    pady=20
)
form.pack(fill="x", pady=10)

tk.Label(
    form,
    text="Student ID:",
    bg="white",
    font=("Segoe UI", 10)
).grid(row=0, column=0, padx=10, pady=10)

entry_id = tk.Entry(form, width=30, font=("Segoe UI", 10))
entry_id.grid(row=0, column=1)

tk.Label(
    form,
    text="Full Name:",
    bg="white",
    font=("Segoe UI", 10)
).grid(row=1, column=0, padx=10, pady=10)

entry_name = tk.Entry(form, width=30, font=("Segoe UI", 10))
entry_name.grid(row=1, column=1)

btn_frame = tk.Frame(form, bg="white")
btn_frame.grid(row=2, column=0, columnspan=2, pady=15)

tk.Button(
    btn_frame,
    text="TIME IN",
    width=15,
    bg="#2e7d32",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=lambda: save_attendance("TIME IN")
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame,
    text="TIME OUT",
    width=15,
    bg="#c62828",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    command=lambda: save_attendance("TIME OUT")
).grid(row=0, column=1, padx=10)

table_frame = tk.LabelFrame(
    main,
    text="Attendance Records",
    font=("Segoe UI", 11, "bold"),
    bg="white"
)
table_frame.pack(fill="both", expand=True, pady=15)

columns = ("ID", "Name", "Status", "Time")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

tree.heading("ID", text="Student ID")
tree.heading("Name", text="Full Name")
tree.heading("Status", text="Status")
tree.heading("Time", text="Date & Time")

tree.column("ID", width=150)
tree.column("Name", width=250)
tree.column("Status", width=120)
tree.column("Time", width=250)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

refresh_table()
update_dashboard()

root.mainloop()