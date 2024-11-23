import json
import os


class Book:

    def __init__(self, book_id, title, author, year, status='В наличии'):
        """
        Класс Book
        Параметр book_id формируется на основе максимального ID в books.json,
        остальные параментры вводятся пользователем в консоли, status по умолчанию
        'В наличии', может иметь только 2 значения.

        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        """
        Создает объект Book из словаря.
        """
        return cls(
            book_id=data['id'],
            title=data['title'],
            author=data['author'],
            year=data['year'],
            status=data.get('status', 'В наличии')
        )


def save_books(books, filename='books.json'):
    """
    Метод для сохранения списка книг в JSON-файл.

    Параметры
    ----------
    books : list
        Список книг
    filename : str, optional
        Путь к JSON-файлу (default: 'books.json')

    Переписывает содержимое JSON-файла, если он уже существует.

    """
    with open(filename, 'w', encoding='utf-8') as f:
        json_books = [book.to_dict() for book in books]
        json.dump(json_books, f, ensure_ascii=False, indent=4)


def load_books(filename='books.json'):
    """"
    Метод для загрузки списка книг из JSON-файла.

    Параметры
    ----------
    filename : str, optional
        Путь к JSON-файлу (default: 'books.json')

    Возвращает список книг из JSON-файла.
    Данные хранятся в виде списка объектов Book в оперативной памяти до следующего сохранения.
    """
    books = []
    if not os.path.exists(filename):
        return books
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return books
            json_books = json.loads(content)
            for data in json_books:
                book = Book.from_dict(data)
                books.append(book)
    except json.JSONDecodeError:
        print("Ошибка: Файл 'books.json' содержит некорректные данные.")
        print("Файл будет перезаписан при следующем сохранении.")
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла: {e}")
    return books


def add_book(books):
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = input("Введите год издания книги: ")
    print()

    # Определяем следующий ID
    if books:
        max_id = max(book.id for book in books)
        new_id = max_id + 1
    else:
        new_id = 1

    new_book = Book(new_id, title, author, year)
    books.append(new_book)
    print(f"Книга добавлена успешно! ID новой книги: {new_book.id}")


def delete_book(books):
    """
    Обработка ошибок реализована из-за возможных ошибок связанных с ID
    """
    try:
        book_id = int(input("Введите ID книги для удаления: "))
        print()
    except ValueError:
        print("ID должен быть числом.")
        return
    for book in books:
        if book.id == book_id:
            books.remove(book)
            input("Книга удалена успешно, нажмите Enter для выхода в меню...")
            return
    input("Книга с указанным ID не найдена, нажмите Enter для выхода в меню...")


def search_book(books):
    title = input("Введите название книги, имя автора или год издания: ")
    print()

    found_books = []
    for book in books:
        if (title.lower() in book.title.lower() or
            title.lower() in book.author.lower() or
                str(book.year).lower() == title.lower()):
            found_books.append(book)

    if found_books:
        print("Найденные книги:")
        print()
        for book in found_books:
            print(f"ID: {book.id}")
            print(f"Название: {book.title}")
            print(f"Автор: {book.author}")
            print(f"Год издания: {book.year}")
            print(f"Статус: {book.status}")
            print()
        input('Нажмите Enter для выхода в меню...')
    else:
        print("Книги не найдены.")


def display_books(books):
    if not books:
        print("Список книг пуст.")
    else:
        print("Список книг:")
        print()
        for book in books:
            print(f"ID: {book.id}")
            print(f"Название: {book.title}")
            print(f"Автор: {book.author}")
            print(f"Год издания: {book.year}")
            print(f"Статус: {book.status}")
            print()
        input('\nНажмите Enter для выхода в меню...')


def change_status(books):
    while True:
        book_id_input = input(
            "Введите ID книги для изменения статуса (нажмите Enter для выхода): ")
        print()
        if not book_id_input:
            print("Возврат в главное меню.")
            return
        if not book_id_input.isdigit():
            print("ID должен быть числом. Попробуйте снова.")
            print()
            continue
        book_id = int(book_id_input)

        # Проверяем, есть ли книга с таким ID
        book = next((book for book in books if book.id == book_id), None)
        if not book:
            print("Книга с указанным ID не найдена. Попробуйте снова.")
            print()
            continue
        else:
            break

    while True:
        new_status = input(
            "Введите новый статус (В наличии/Выдана) или нажмите Enter для выхода: ")

        if not new_status:
            print("Возврат в главное меню.")
            return
        if new_status not in ['В наличии', 'Выдана']:
            print("Некорректный статус. Попробуйте снова.")
            continue
        else:
            break
    print()
    book.status = new_status
    print("Статус книги изменен успешно!")

    input('\nНажмите Enter для выхода в меню...')


def main():
    books = load_books()
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Показать список книг")
        print("5. Изменить статус книги")
        print("6. Выход")
        print()
        choice = input("Выберите действие: ")
        print()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            delete_book(books)
        elif choice == "3":
            search_book(books)
        elif choice == "4":
            display_books(books)
        elif choice == "5":
            change_status(books)
        elif choice == "6":
            save_books(books)
            print("Данные сохранены. Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
