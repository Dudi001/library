import os
import json


class BookAttribute:
    """Класс, представляющий атрибуты книги в библиотеке.

    Методы:
        * from_dict() - создает экземпляр BookAttribute из словаря
        * to_dict() - возвращает словарь с данными книги
    """
    def __init__(
            self,
            id: int,
            title: str,
            author: str,
            year: int,
            status="в наличии"
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """Возвращает словарь с данными книги"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        """Создает экземпляр BookAttribute из словаря"""

        return BookAttribute(
            data["id"],
            data["title"],
            data["author"],
            data["year"],
            data["status"]
        )


LIBRARY = "library.json"


class WorkWithLibrary():

    """Класс для работы с библиотекой.

        Методы:
        * load_library() - загружает библиотеку из файла JSON.
        * save_library() - Сохраняет библиотеку в файл JSON.
        * get_next_book_id() - Возвращает следующий id для книги.
        * add_book() - Метод добавляет книгу в библиотеку.
        * delete_book() - Удаляет книгу из библиотеки по id.
        * find_books() - Ищет книги по заданному полю (title, author или year).
        * display_books() - Отображает список всех книг в библиотеке.
        * update_status() - Изменяет статус книги по id.
    """

    def load_library(self) -> list:
        """Загружает библиотеку из файла JSON.

        :return: список книг
        """

        if not os.path.exists(LIBRARY):
            return []
        with open(LIBRARY, "r", encoding="utf-8") as f:
            return [BookAttribute.from_dict(book) for book in json.load(f)]

    def save_library(
            self,
            library: list
    ):
        """Сохраняет библиотеку в файл JSON.

        :param library: список книг
        """

        with open(LIBRARY, "w", encoding="utf-8") as f:
            json.dump(
                [book.to_dict() for book in library],
                f,
                ensure_ascii=False, indent=4
            )

    def get_next_book_id(
            self,
            library: list
    ) -> int:
        """Возвращает следующий уникальный идентификатор для книги.

        :param library: список книг
        :return: индекс
        """
        if not library:
            return 1
        return max(book.id for book in library) + 1

    def add_book(
            self,
            title: str,
            author: str,
            year: int
    ):
        """Метод добавляет книгу в библиотеку.

        :param title: наименование книги
        :param author: автор книги
        :param year: год выпуска книги
        """

        library = self.load_library()
        book_id = self.get_next_book_id(library)
        new_book = BookAttribute(book_id, title, author, year)
        library.append(new_book)
        self.save_library(library)
        print(f"Книга '{title}' добавлена. \nЕё id: {book_id}")

    def delete_book(
            self,
            book_id: int
    ):
        """Удаляет книгу из библиотеки по id.

        :param book_id: уникальный идентификатор книги
        """

        library = self.load_library()
        library = [book for book in library if book.id != book_id]
        self.save_library(library)
        print(f"\nКнига с id {book_id} удалена \n")

    def find_books(
            self,
            query: str,
            by="title"
    ) -> list:
        """Ищет книги по заданному полю (title, author или year).

        :param query: запрос
        :return: список найденных книг
        """

        library = self.load_library()
        results = [
            book for book in library
            if query.lower() in str(getattr(book, by)).lower()
        ]
        return results

    def display_books(self):
        """Отображает список всех книг в библиотеке."""

        library = self.load_library()
        if not library:
            print("\nБиблиотека пуста.")
            return
        for book in library:
            print(
                f"id: {book.id} Название: '{book.title}' Автор: {book.author}, Год: {book.year},  {book.status}"
            )

    def update_status(
            self,
            book_id: int,
            new_status: str
    ):
        """Изменяет статус книги по id.

        :param book_id: уникальный идентификатор книги
        :param new_status: статус книги
        """

        library = self.load_library()
        for book in library:
            if book.id == book_id:
                book.status = new_status
                self.save_library(library)
                print(
                    f"\n Статус книги с id {book_id} изменён на '{new_status}'"
                )
                return
        print(f"\nКнига с id {book_id} не найдена")


def main():
    """Главная функция для взаимодействия с пользователем через консоль."""

    work_with_library = WorkWithLibrary()
    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите опцию: ")

        if choice == "1":
            title: str = input("Введите название книги: ")
            author: str = input("Введите автора книги: ")
            try:
                year: int = int(input("Введите год издания книги: "))
                work_with_library.add_book(title, author, year)
            except ValueError:
                print("Введите год цифрами")
        elif choice == "2":
            try:
                book_id = int(input("Введите id книги для удаления: "))
                work_with_library.delete_book(book_id)
            except ValueError:
                print(
                    "\nНекорректный id. Пожалуйста, введите числовое значение."
                )
        elif choice == "3":
            query = input("Введите запрос для поиска книги: ")
            by = input("Искать по (title, author, year): ")
            if by not in ["title", "author", "year"]:
                print(
                    "Некорректное поле поиска. Пожалуйста, выберите title, author или year."
                )
                continue
            results = work_with_library.find_books(query, by)
            if results:
                for book in results:
                    print(
                        f"id: {book.id} Название: '{book.title}' Автор: {book.author}, Год: {book.year},  {book.status}"
                    )
            else:
                print("Книги не найдены.")
        elif choice == "4":
            work_with_library.display_books()
        elif choice == "5":
            try:
                book_id = int(
                    input("Введите id книги для изменения статуса: ")
                )
                new_status = input(
                    "Введите новый статус ('в наличии' или 'выдана'): "
                )
                if new_status not in ["в наличии", "выдана"]:
                    print(
                        "Некорректный статус. Пожалуйста, введите 'в наличии' или 'выдана'."
                    )
                    continue
                work_with_library.update_status(book_id, new_status)
            except ValueError:
                print(
                    "\nНекорректный id. Пожалуйста, введите числовое значение."
                )
        elif choice == "6":
            break
        else:
            print("\n Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
