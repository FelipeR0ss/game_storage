import tkinter as tk
from tkinter import messagebox, filedialog
import os

STORAGE = {}


def load_data():
    try:
        if not os.path.exists('database.csv'):
            with open('database.csv', 'w') as file:
                pass
            messagebox.showinfo(
                "Load Data", "Database file created as it did not exist.")
            return

        with open('database.csv', 'r') as file:
            lines = file.readlines()
            for line in lines:
                details = line.strip().split(',')
                if len(details) == 5:
                    game, gender, initializer, status, note = details
                    STORAGE[game] = {
                        'gender': gender, 'initializer': initializer, 'status': status, 'note': note}
                else:
                    print(f"Warning: Skipping malformed line: {line.strip()}")
        messagebox.showinfo("Load Data", "Database loaded successfully!")
    except Exception as error:
        messagebox.showerror("Load Data", f"An error occurred: {error}")


def save_data():
    try:
        with open('database.csv', 'w') as file:
            for game, details in STORAGE.items():
                line = f"{game},{details['gender']},{details['initializer']},{details['status']},{details['note']}\n"
                file.write(line)
        messagebox.showinfo("Save Data", "Data saved successfully!")
    except Exception as error:
        messagebox.showerror("Save Data", f"An error occurred: {error}")


def add_game():
    game = entry_game_name.get()
    gender = entry_gender.get()
    initializer = entry_initializer.get()
    status = entry_status.get()
    note = entry_note.get()

    if game:
        STORAGE[game] = {
            'gender': gender, 'initializer': initializer, 'status': status, 'note': note}
        save_data()
        list_games()
        clear_entries()
        messagebox.showinfo("Add Game", f"Game '{game}' added successfully!")
    else:
        messagebox.showwarning("Add Game", "Game name is required!")


def edit_game():
    game = entry_game_name.get()
    if game in STORAGE:
        STORAGE[game]['gender'] = entry_gender.get()
        STORAGE[game]['initializer'] = entry_initializer.get()
        STORAGE[game]['status'] = entry_status.get()
        STORAGE[game]['note'] = entry_note.get()
        save_data()
        list_games()
        clear_entries()
        messagebox.showinfo("Edit Game", f"Game '{game}' edited successfully!")
    else:
        messagebox.showwarning("Edit Game", f"Game '{game}' not found!")


def delete_game():
    game = entry_game_name.get()
    if game in STORAGE:
        del STORAGE[game]
        save_data()
        list_games()
        clear_entries()
        messagebox.showinfo(
            "Delete Game", f"Game '{game}' deleted successfully!")
    else:
        messagebox.showwarning("Delete Game", f"Game '{game}' not found!")


def export_games():
    file_name = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_name:
        try:
            with open(file_name, 'w') as file:
                for game, details in STORAGE.items():
                    line = f"{game},{details['gender']},{details['initializer']},{details['status']},{details['note']}\n"
                    file.write(line)
            messagebox.showinfo("Export Data", "Data exported successfully!")
        except Exception as error:
            messagebox.showerror("Export Data", f"An error occurred: {error}")


def import_games():
    file_name = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_name:
        try:
            with open(file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    details = line.strip().split(',')
                    game, gender, initializer, status, note = details
                    STORAGE[game] = {
                        'gender': gender, 'initializer': initializer, 'status': status, 'note': note}
            save_data()
            list_games()
            messagebox.showinfo("Import Data", "Data imported successfully!")
        except Exception as error:
            messagebox.showerror("Import Data", f"An error occurred: {error}")


def list_games():
    games_list.delete(0, tk.END)
    for game in STORAGE:
        games_list.insert(tk.END, game)


def show_game_details(event):
    selected_game = games_list.get(games_list.curselection())
    details = STORAGE[selected_game]
    entry_game_name.delete(0, tk.END)
    entry_game_name.insert(0, selected_game)
    entry_gender.delete(0, tk.END)
    entry_gender.insert(0, details['gender'])
    entry_initializer.delete(0, tk.END)
    entry_initializer.insert(0, details['initializer'])
    entry_status.delete(0, tk.END)
    entry_status.insert(0, details['status'])
    entry_note.delete(0, tk.END)
    entry_note.insert(0, details['note'])


def clear_entries():
    entry_game_name.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_initializer.delete(0, tk.END)
    entry_status.delete(0, tk.END)
    entry_note.delete(0, tk.END)


# GUI Setup
root = tk.Tk()
root.title("Game Catalog")

# Input
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Game Name").grid(row=0, column=0)
entry_game_name = tk.Entry(frame)
entry_game_name.grid(row=0, column=1)

tk.Label(frame, text="Gender").grid(row=1, column=0)
entry_gender = tk.Entry(frame)
entry_gender.grid(row=1, column=1)

tk.Label(frame, text="Initializer").grid(row=2, column=0)
entry_initializer = tk.Entry(frame)
entry_initializer.grid(row=2, column=1)

tk.Label(frame, text="Status").grid(row=3, column=0)
entry_status = tk.Entry(frame)
entry_status.grid(row=3, column=1)

tk.Label(frame, text="Note").grid(row=4, column=0)
entry_note = tk.Entry(frame)
entry_note.grid(row=4, column=1)

# Buttons
tk.Button(root, text="Add Game", command=add_game).pack(fill=tk.X, pady=2)
tk.Button(root, text="Edit Game", command=edit_game).pack(fill=tk.X, pady=2)
tk.Button(root, text="Delete Game",
          command=delete_game).pack(fill=tk.X, pady=2)
tk.Button(root, text="Export Data",
          command=export_games).pack(fill=tk.X, pady=2)
tk.Button(root, text="Import Data",
          command=import_games).pack(fill=tk.X, pady=2)

# Game List
games_list = tk.Listbox(root)
games_list.pack(fill=tk.BOTH, expand=True)
games_list.bind("<<ListboxSelect>>", show_game_details)

# Load
load_data()
list_games()

root.mainloop()
