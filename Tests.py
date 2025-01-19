import unittest
from unittest.mock import patch, MagicMock
from app import App
from users import User
from trains import Train

class TestApp(unittest.TestCase):

    def setUp(self):
        # Создаем объект приложения
        self.app = App()
        self.app.users = [User(username="test_user1", password="1234")]
        self.app.trains = [
            Train(number="101", departure_date="2025-01-20", departure_time="10:00",
                  origin="CityA", destination="CityB", seats=10)
        ]

    def test_login_success(self):
        """Тест успешного входа пользователя."""
        print("\n=== Тест: Успешный вход пользователя ===")
        print("Начало теста: test_login_success")
        with patch("tkinter.messagebox.showerror") as mock_error, \
                patch("tkinter.messagebox.showinfo") as mock_info:
            self.app.username_entry = MagicMock()
            self.app.password_entry = MagicMock()
            self.app.username_entry.get.return_value = "test_user1"
            self.app.password_entry.get.return_value = "1234"

            self.app.login()

            # Убеждаемся, что ошибок не было и пользователь вошел успешно
            mock_error.assert_not_called()
            self.assertEqual(self.app.current_user.username, "test_user1")
        print("Окончание теста: test_login_success")

    def test_register_existing_user(self):
        """Тест регистрации с существующим именем пользователя."""
        print("\n=== Тест: Регистрация с существующим именем пользователя ===")
        print("Начало теста: test_register_existing_user")
        with patch("tkinter.messagebox.showerror") as mock_error:
            self.app.reg_username_entry = MagicMock()
            self.app.reg_password_entry = MagicMock()
            self.app.reg_username_entry.get.return_value = "test_user1"
            self.app.reg_password_entry.get.return_value = "abcd"

            self.app.register()

            # Проверяем, что регистрация провалилась
            mock_error.assert_called_once_with("Ошибка!", "Имя пользователя уже существует")
        print("Окончание теста: test_register_existing_user")

    def test_book_ticket_no_seats(self):
        """Тест бронирования билета, когда мест нет."""
        print("\n=== Тест: Бронирование билета при отсутствии мест ===")
        print("Начало теста: test_book_ticket_no_seats")
        self.app.trains[0].seats = 0

        with patch("tkinter.messagebox.showerror") as mock_error:
            self.app.train_booking_entry = MagicMock()
            self.app.train_booking_entry.get.return_value = "101"

            self.app.book_ticket()

            # Проверяем, что возникла ошибка из-за отсутствия мест
            mock_error.assert_called_once_with("Ошибка!", "Нет свободных мест")
        print("Окончание теста: test_book_ticket_no_seats")

    def test_fail_example(self):
        """Тест, который проверяет бронирование и падает."""
        print("\n=== Тест: Проверка бронирования и намеренное падение ===")
        print("Начало теста: test_fail_example")

        self.app.train_booking_entry = MagicMock()
        self.app.train_booking_entry.get.return_value = "999"  # Несуществующий номер поезда

        with patch("tkinter.messagebox.showerror") as mock_error:
            self.app.book_ticket()

            # Ошибка возникает, так как поезд с номером 999 не существует
            mock_error.assert_called_once_with("Ошибка!", "Поезд не найден")
            self.assertEqual(self.app.trains[0].seats, 0, "Поезд с номером 999 найден, но не должен существовать")
        print("Окончание теста: test_fail_example")


if __name__ == "__main__":
    unittest.main()