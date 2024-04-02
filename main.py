import sqlite3

PHONEBOOK_DB = "phonebook.db"

def create_phonebook_table():
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Phonebook (
                        Name TEXT PRIMARY KEY,
                        Number TEXT
                    )''')
    conn.commit()
    conn.close()

def load_phonebook_from_db():
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Phonebook")
    phonebook = {name: number for name, number in cursor.fetchall()}
    conn.close()
    return phonebook

def save_contact_to_db(name, number):
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO Phonebook (Name, Number) VALUES (?, ?)", (name, number))
    conn.commit()
    conn.close()

def delete_contact_from_db(name):
    conn = sqlite3.connect(PHONEBOOK_DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Phonebook WHERE Name = ?", (name,))
    conn.commit()
    conn.close()

def search_contact(phonebook, name):
    if name in phonebook:
        print(f"Номер телефона для {name}: {phonebook[name]}")
    else:
        print("Контакт не найден.")

def search_by_number(phonebook, number):
    found_contacts = []
    for name, phone_number in phonebook.items():
        if phone_number == number:
            found_contacts.append(name)
    if found_contacts:
        print(f"Найдены контакты с номером {number}:")
        for contact_name in found_contacts:
            print(contact_name)
    else:
        print(f"Контакт с номером {number} не найден.")

def list_contacts(phonebook):
    if phonebook:
        print("Телефонный справочник:")
        for name, number in phonebook.items():
            print(f"{name}: {number}")
    else:
        print("Телефонный справочник пуст.")

def main():
    create_phonebook_table()
    phonebook = load_phonebook_from_db()
    while True:
        print("\nМеню:")
        print("1. Просмотреть контакты")
        print("2. Добавить контакт")
        print("3. Удалить контакт")
        print("4. Поиск контакта по имени")
        print("5. Поиск контакта по номеру")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            list_contacts(phonebook)
        elif choice == "2":
            name = input("Введите имя: ")
            number = input("Введите номер телефона: ")
            save_contact_to_db(name, number)
            print("Контакт успешно добавлен.")
        elif choice == "3":
            name = input("Введите имя контакта для удаления: ")
            delete_contact_from_db(name)
            print("Контакт успешно удален.")
        elif choice == "4":
            name = input("Введите имя контакта для поиска: ")
            search_contact(phonebook, name)
        elif choice == "5":
            number = input("Введите номер телефона для поиска: ")
            search_by_number(phonebook, number)
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
