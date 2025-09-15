import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ----------------- Functions -----------------
def add_task():
    task = task_entry.get()
    category = category_entry.get()
    if task and category:
        tree.insert("", tk.END, values=(task, "pending", category))
        task_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Enter both Task and Category")

def mark_done():
    selected = tree.selection()
    if selected:
        for item in selected:
            tree.set(item, column="Status", value="done")
    else:
        messagebox.showinfo("Info", "Select a task to mark done")

def delete_task():
    selected = tree.selection()
    if selected:
        for item in selected:
            tree.delete(item)
    else:
        messagebox.showinfo("Info", "Select a task to delete")

# ----------------- Main Window -----------------
root = tk.Tk()
root.title("Anime Dark To-Do App")
root.geometry("600x400")
root.configure(bg="#1E1E2F")  # dark background color

# ----------------- Styles -----------------
style = ttk.Style(root)
style.theme_use("clam")  # clean theme
style.configure("Treeview",
                background="#2E2E3F",
                foreground="white",
                rowheight=25,
                fieldbackground="#2E2E3F")
style.configure("Treeview.Heading",
                background="#444466",
                foreground="white",
                font=('Arial', 12, 'bold'))

# ----------------- Input Frame -----------------
input_frame = tk.Frame(root, bg="#1E1E2F")
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=30, bg="#2E2E3F", fg="white", insertbackground="white")
task_entry.grid(row=0, column=0, padx=5)

category_entry = tk.Entry(input_frame, width=20, bg="#2E2E3F", fg="white", insertbackground="white")
category_entry.grid(row=0, column=1, padx=5)

add_btn = tk.Button(input_frame, text="Add Task", bg="#6C63FF", fg="white", command=add_task)
add_btn.grid(row=0, column=2, padx=5)

done_btn = tk.Button(input_frame, text="Mark Done", bg="#00C851", fg="white", command=mark_done)
done_btn.grid(row=1, column=0, pady=5)

delete_btn = tk.Button(input_frame, text="Delete Task", bg="#ff4444", fg="white", command=delete_task)
delete_btn.grid(row=1, column=1, pady=5)

# ----------------- Treeview -----------------
columns = ("Task", "Status", "Category")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

# Optional: add some anime-style font
tree.tag_configure('anime', font=('Comic Sans MS', 10, 'bold'))

root.mainloop()
