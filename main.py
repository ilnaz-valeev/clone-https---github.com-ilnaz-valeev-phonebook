import tkinter as tk
from tkinter import messagebox
import sqlite3

PHONEBOOK_DB = "phonebook.db"

def create_phonebook_table():
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Phonebook (
                        Name TEXT,
                        Number TEXT
                    )''')
    conn.commit()
    conn.close()

def save_contact(name, number):
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Phonebook (Name, Number) VALUES (?, ?)", (name, number))
    conn.commit()
    conn.close()

def delete_contact(name, number):
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Phonebook WHERE Name = ? AND Number = ?", (name, number))
    conn.commit()
    conn.close()

def search_contact(name):
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Phonebook WHERE Name = ?", (name,))
    results = cursor.fetchall()
    conn.close()
    return results

def list_contacts():
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Phonebook ORDER BY Name")
    phonebook = cursor.fetchall()
    conn.close()
    return phonebook

def add_contact(name_entry, number_entry):
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        existing_contacts = search_contact(name)
        if existing_contacts:
            existing_numbers = [contact[1] for contact in existing_contacts]
            if number not in existing_numbers:
                save_contact(name, number)
                messagebox.showinfo("Успех", "Контакт успешно добавлен.")
            else:
                messagebox.showerror("Ошибка", "Такой номер уже существует для этого имени.")
        else:
            save_contact(name, number)
            messagebox.showinfo("Успех", "Контакт успешно добавлен.")
        clear_entries(name_entry, number_entry)
    else:
        messagebox.showerror("Ошибка", "Необходимо ввести и имя, и номер телефона.")

def remove_contact(name_entry, number_entry):
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        delete_contact(name, number)
        messagebox.showinfo("Успех", "Контакт успешно удален.")
        clear_entries(name_entry, number_entry)
    else:
        messagebox.showerror("Ошибка", "Необходимо ввести и имя, и номер телефона.")

def find_contact(name_entry):
    name = name_entry.get()
    results = search_contact(name)
    if results:
        result_text = ""
        for result in results:
            result_text += f"Имя: {result[0]}, Номер: {result[1]}\n"
        messagebox.showinfo("Результат", result_text)
    else:
        messagebox.showinfo("Результат", "Контакт не найден.")
    clear_entries(name_entry, number_entry)

def show_contacts():
    contacts = list_contacts()
    if contacts:
        result = ""
        for contact in contacts:
            result += f"Имя: {contact[0]}, Номер: {contact[1]}\n"
        messagebox.showinfo("Телефонный справочник", result)
    else:
        messagebox.showinfo("Телефонный справочник", "Телефонный справочник пуст.")

def clear_entries(name_entry, number_entry):
    name_entry.delete(0, tk.END)
    number_entry.delete(0, tk.END)

def edit_contact(name_entry, number_entry):
    name = name_entry.get()
    number = number_entry.get()
    if name and number:
        conn = sqlite3.connect(PHONEBOOK_DB)
        cursor = conn.cursor()
        cursor.execute("UPDATE Phonebook SET Number = ? WHERE Name = ?", (number, name))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Контакт успешно отредактирован.")
        clear_entries(name_entry, number_entry)
    else:
        messagebox.showerror("Ошибка", "Необходимо ввести и имя, и номер телефона.")


def create_gui():
    root = tk.Tk()
    root.title("Телефонный справочник")

    label_name = tk.Label(root, text="Имя:", font=("Helvetica", 12))
    label_name.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    name_entry = tk.Entry(root, font=("Helvetica", 12))
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    label_number = tk.Label(root, text="Номер:", font=("Helvetica", 12))
    label_number.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    number_entry = tk.Entry(root, font=("Helvetica", 12))
    number_entry.grid(row=1, column=1, padx=5, pady=5)

    button_add = tk.Button(root, text="Добавить", font=("Helvetica", 12), command=lambda: add_contact(name_entry, number_entry))
    button_add.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    button_remove = tk.Button(root, text="Удалить", font=("Helvetica", 12), command=lambda: remove_contact(name_entry, number_entry))
    button_remove.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    button_find = tk.Button(root, text="Найти", font=("Helvetica", 12), command=lambda: find_contact(name_entry))
    button_find.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    button_edit = tk.Button(root, text="Редактировать", font=("Helvetica", 12), command=lambda: edit_contact(name_entry, number_entry))
    button_edit.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    button_show = tk.Button(root, text="Показать все", font=("Helvetica", 12), command=show_contacts)
    button_show.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    button_exit = tk.Button(root, text="Выход", font=("Helvetica", 12), command=root.quit)
    button_exit.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_phonebook_table()
    create_gui()
