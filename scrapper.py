import tkinter as tk
from tkinter import ttk, messagebox
from scrapper_backend import get_product_info, save_links_to_db, refresh_all, delete_from_db, is_valid_url
from sqlite3 import IntegrityError

def add_product():
    popup = tk.Toplevel(root)
    popup.title("Add link")
    popup.geometry("400x150")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()
    
    label = tk.Label(popup, text="Enter link: ")
    label.pack(pady=10)
    
    entry = tk.Entry(popup, width=50)
    entry.pack(pady=5)
    
    def save():
        link = entry.get().strip()
        if not link:
            messagebox.showwarning("Error", "Link entry cannot be empty")
        elif not is_valid_url(link):
            messagebox.showerror("Błąd", "Podaj poprawny URL zaczynający się od http:// lub https://")
        else:
            try:
                save_links_to_db(link)
                refresh_all(tree)
                popup.destroy()
            except IntegrityError:
                messagebox.showerror("Error", "The link is already in database")
    
    button = tk.Button(popup, text="Save", command=save)
    button.pack(pady=10)
    
def on_right_click(event):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        tree.selection_set(selected_item)
        popup_menu.post(event.x_root, event.y_root)    

def delete_selected_item():
    selected_item = tree.selection()
    url_to_delete = selected_item[0]
    delete_from_db(url_to_delete)
    tree.delete(selected_item)

root = tk.Tk()
root.title("Morele web scrapper")
root.geometry("1200x500")
root.resizable(False, False)

main_frame = tk.Frame(root)
main_frame.pack(fill="both", padx=10, pady=10, expand=True)

list_frame = tk.Frame(main_frame)
tree = ttk.Treeview(main_frame, columns=("Name", "Price"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.pack(fill="both", expand=True)
tree.bind("<Button-3>", on_right_click)

popup_menu = tk.Menu(root, tearoff=0)
popup_menu.add_command(label="delete", command=delete_selected_item)


button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add product", width=80, command=add_product)
add_button.pack(side="left", padx=5)

refresh_button = tk.Button(button_frame, text="Refresh list", width=80, command=lambda: refresh_all(tree))
refresh_button.pack(side="right", padx=5)





root.mainloop()