import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Global Variables
df_original = pd.DataFrame()
df_displayed = pd.DataFrame()
filter_criteria = []        # List tuples (Column, Keyword)

# Import CSV 
def import_csv():
    global df_original, df_displayed, filter_criteria
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        
        df_original = pd.read_csv(file_path)
        df_displayed = df_original.copy()
        filter_criteria.clear()

        update_treeview(df_displayed)
        update_filter_options()
        update_filter_listbox()
    
    except Exception as e:
        messagebox.showerror("Error Import: ",str(e))

# Display in Treeview
def update_treeview(df):
    try:
        tree.delete(*tree.get_children())
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        for col in df.columns:
            tree.heading(col, text=col, command=lambda c=col: sort_column(c))
            tree.column(col, anchor="center")

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    except Exception as e:
        messagebox.showerror("Error Display", str(e))

# Sort
def sort_column(col):
    global df_displayed
    try:
        df_displayed = df_displayed.sort_values(by=col, ascending=True)
        update_treeview(df_displayed)
    except Exception as e:
        messagebox.showerror("Erreur Tri", str(e))

# Update list of columns for filter
def update_filter_options():
    try:
        filter_column_cb["values"] = list(df_original.columns)
        if not df_original.empty:
            filter_column_cb.current(0)
    except Exception:
        pass

# Add criteria of filter
def add_filter():
    col = filter_column_cb.get()
    val = filter_entry.get()
    if col and val:
        filter_criteria.append((col, val))
        update_filter_listbox()
        apply_filters()


# Delete criteria selected
def remove_filter():
    try:
        idx = filter_listbox.curselection()
        if idx:
            del filter_criteria[idx[0]]
            update_filter_listbox()
            apply_filters()
    except Exception as e:
        messagebox.showerror("Erreur Supression", str(e))

# Update filter listbox
def update_filter_listbox():
    filter_listbox.delete(0, tk.END)
    for col, val in filter_criteria:
        filter_listbox.insert(tk.END, f"{col} contient {val}")

# Apply filter accumulated
def apply_filters():
    global df_displayed
    try:
        df = df_original.copy()
        for col, val in filter_criteria:
            df = df[df[col].astype(str).str.lower().str.contains(val.lower())]
        df_displayed = df
        update_treeview(df_displayed)
    except Exception as e:
        messagebox.showerror("Error Filter", str(e))

# Global Search
def search_data(event=None):
    global df_displayed
    try:
        keyword = search_entry.get().lower()
        if keyword:
            mask = df_original.apply(lambda row: row.astype(str).str.lower().str.contains(keyword).any(), axis=1)
            df_displayed = df_original[mask]
        else:
            df_displayed = df_original.copy()
        update_treeview(df_displayed)
    except Exception as e:
        messagebox.showerror("Error Search", str(e))


# Export to CSV
def export_csv():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            df_displayed.to_csv(file_path, index=False)
            messagebox.showinfo("Succes", "File exported succesfull.")
    except Exception as e:
        messagebox.showerror("Error Export", str(e))

# Reset
def reset_filter():
    global df_displayed, filter_criteria
    filter_criteria.clear()
    update_filter_listbox()
    df_displayed = df_original
    update_treeview(df_displayed)


# Interface principal
root = tk.Tk()
root.title("Gestion CSV")
root.geometry("1000x650")

# Buttons import/export
top_frame = tk.Frame(root)
top_frame.pack(pady=5)
tk.Button(top_frame, text="Importer CSV", command=import_csv).grid(row=0, column=0, padx=5)
tk.Button(top_frame, text="Exporter CSV", command=export_csv).grid(row=0, column=1, padx=5)

# Global Search
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search").pack(side="left")
search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", padx=5)
search_entry.bind("<KeyRelease>", search_data)

# Multi-criteria Filter
filter_frame = tk.LabelFrame(root, text="Multiple criteria Filter")
filter_frame.pack(pady=10, fill="both", padx=10)

tk.Label(filter_frame, text="Column: " ).grid(row=0, column=0)
filter_column_cb = ttk.Combobox(filter_frame, width=20)
filter_column_cb.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Keyword: ").grid(row=0, column=2)
filter_entry = tk.Entry(filter_frame, width=20)
filter_entry.grid(row=0, column=3, padx=5)

tk.Button(filter_frame, text="Add Filter", command=add_filter).grid(row=0, column=4, padx=5)
tk.Button(filter_frame, text="Remove Filter", command=remove_filter).grid(row=0, column=5, padx=5)
tk.Button(filter_frame, text="Reinitialize", command=reset_filter).grid(row=0, column=6, padx=5)

filter_listbox = tk.Listbox(filter_frame, height=5, width=80)
filter_listbox.grid(row=1, column=0, columnspan=6, pady=5)

# Table
tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both", padx=10, pady=10)

# Start App
root.mainloop()







