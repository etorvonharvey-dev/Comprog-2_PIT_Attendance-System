import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def mark_attendance():
    name = entry_name.get()

    if name.strip() == "":
        messagebox.showerror("Error", "Please enter a name.")
        return

    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("attendance.txt", "a") as file:
            file.write(f"{name} - {current_time}\n")

        messagebox.showinfo("Success", "Attendance recorded!")
        entry_name.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


def view_records():
    try:
        with open("attendance.txt", "r") as file:
            records = file.read()

        if records.strip() == "":
            records = "No records found."

        view_window = tk.Toplevel(root)
        view_window.title("Attendance Records")

        text_area = tk.Text(view_window, width=40, height=15)
        text_area.pack()
        text_area.insert(tk.END, records)

    except FileNotFoundError:
        messagebox.showerror("Error", "No attendance file found.")



root = tk.Tk()
root.title("Attendance System")
root.geometry("300x180")

label_title = tk.Label(root, text="Attendance System", font=("Arial", 14))
label_title.grid(row=0, column=0, columnspan=2, pady=10)

label_name = tk.Label(root, text="Name:")
label_name.grid(row=1, column=0, padx=10, pady=5)

entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1)

btn_mark = tk.Button(root, text="Mark Attendance", command=mark_attendance)
btn_mark.grid(row=2, column=0, columnspan=2, pady=10)

btn_view = tk.Button(root, text="View Records", command=view_records)
btn_view.grid(row=3, column=0, columnspan=2)

root.mainloop()