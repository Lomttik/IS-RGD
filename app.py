import json
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from users import User
from trains import Train

class App:
    def __init__(self):
        self.users_file = "users.json"
        self.trains_file = "trains.json"
        self.current_user = None

        self.users = self.load_users()
        self.trains = self.load_trains()

        self.root = ctk.CTk()
        self.root.title("Train Booking System")
        self.build_login_screen()

    def load_users(self):
        try:
            with open(self.users_file, "r") as file:
                return [User(**user) for user in json.load(file)]
        except FileNotFoundError:
            return []

    def save_users(self):
        with open(self.users_file, "w") as file:
            json.dump([user.to_dict() for user in self.users], file)

    def load_trains(self):
        try:
            with open(self.trains_file, "r") as file:
                return [Train(**train) for train in json.load(file)]
        except FileNotFoundError:
            return []

    def save_trains(self):
        with open(self.trains_file, "w") as file:
            json.dump([train.to_dict() for train in self.trains], file)

    def build_login_screen(self):
        self.clear_screen()

        ctk.CTkLabel(self.root, text="Вход", font=("Arial", 20)).pack(pady=10)
        self.username_entry = ctk.CTkEntry(self.root, placeholder_text="ФИО")
        self.username_entry.pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.root, placeholder_text="Пароль", show="*")
        self.password_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Вход", command=self.login).pack(pady=5)
        ctk.CTkButton(self.root, text="Регистрация", command=self.build_registration_screen).pack(pady=5)

    def build_registration_screen(self):
        self.clear_screen()

        ctk.CTkLabel(self.root, text="Регистрация", font=("Arial", 20)).pack(pady=10)
        self.reg_username_entry = ctk.CTkEntry(self.root, placeholder_text="ФИО")
        self.reg_username_entry.pack(pady=5)
        self.reg_password_entry = ctk.CTkEntry(self.root, placeholder_text="Пароль", show="*")
        self.reg_password_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Регистрация", command=self.register).pack(pady=5)
        ctk.CTkButton(self.root, text="Назад", command=self.build_login_screen).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = next((u for u in self.users if u.username == username and u.password == password), None)
        if user:
            self.current_user = user
            if user.is_admin:
                self.build_admin_dashboard()
            else:
                self.build_user_dashboard()
        else:
            messagebox.showerror("Ошибка!", "Не верные учетные данные")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if any(u.username == username for u in self.users):
            messagebox.showerror("Ошибка!", "Имя пользователя уже существует")
        else:
            new_user = User(username, password)
            self.users.append(new_user)
            self.save_users()
            messagebox.showinfo("Успешно!", "Регистрация прошла успешно")
            self.build_login_screen()

    def build_admin_dashboard(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text=f"Добро пожаловать, {self.current_user.username}!", font=("Arial", 20)).pack(pady=10)
        ctk.CTkButton(self.root, text="Управление отправлениями", command=self.manage_trains).pack(pady=5)
        ctk.CTkButton(self.root, text="Выход", command=self.build_login_screen).pack(pady=5)

    def manage_trains(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="Управление отправлениями", font=("Arial", 20)).pack(pady=10)

        ctk.CTkButton(self.root, text="Создать рейс", command=self.add_train).pack(pady=5)
        ctk.CTkButton(self.root, text="Изменить рейс", command=self.edit_train).pack(pady=5)
        ctk.CTkButton(self.root, text="Удалить рейс", command=self.delete_train).pack(pady=5)
        ctk.CTkButton(self.root, text="Назад", command=self.build_admin_dashboard).pack(pady=5)

    def add_train(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="Создать рейс", font=("Arial", 20)).pack(pady=10)

        self.train_number_entry = ctk.CTkEntry(self.root, placeholder_text="Номер рейса")
        self.train_number_entry.pack(pady=5)
        self.train_date_entry = ctk.CTkEntry(self.root, placeholder_text="Дата отправления (гггг-мм-дд)")
        self.train_date_entry.pack(pady=5)
        self.train_time_entry = ctk.CTkEntry(self.root, placeholder_text="Время отправления (чч:мм)")
        self.train_time_entry.pack(pady=5)
        self.train_origin_entry = ctk.CTkEntry(self.root, placeholder_text="Место оправления")
        self.train_origin_entry.pack(pady=5)
        self.train_destination_entry = ctk.CTkEntry(self.root, placeholder_text="Место прибытия")
        self.train_destination_entry.pack(pady=5)
        self.train_seats_entry = ctk.CTkEntry(self.root, placeholder_text="Места")
        self.train_seats_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Сохранить", command=self.save_new_train).pack(pady=5)
        ctk.CTkButton(self.root, text="Назад", command=self.manage_trains).pack(pady=5)

    def save_new_train(self):
        number = self.train_number_entry.get()
        date = self.train_date_entry.get()
        time = self.train_time_entry.get()
        origin = self.train_origin_entry.get()
        destination = self.train_destination_entry.get()
        seats = self.train_seats_entry.get()

        if not all([number, date, time, origin, destination, seats]):
            messagebox.showerror("Ошибка!", "All fields are required")
            return

        try:
            seats = int(seats)
            new_train = Train(number, date, time, origin, destination, seats)
            self.trains.append(new_train)
            self.save_trains()
            messagebox.showinfo("Успешно!", "Поезд успешно добавлен")
            self.manage_trains()
        except ValueError:
            messagebox.showerror("Ошибка!", "Место: должно быть число")

    def edit_train(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="Изменить рейс", font=("Arial", 20)).pack(pady=10)

        self.edit_train_number_entry = ctk.CTkEntry(self.root, placeholder_text="Номер поезда")
        self.edit_train_number_entry.pack(pady=5)
        ctk.CTkButton(self.root, text="Загрузка", command=self.load_train_for_edit).pack(pady=5)
        ctk.CTkButton(self.root, text="Назад", command=self.manage_trains).pack(pady=5)

    def load_train_for_edit(self):
        number = self.edit_train_number_entry.get()
        train = next((t for t in self.trains if t.number == number), None)

        if train:
            self.clear_screen()
            ctk.CTkLabel(self.root, text=f"Изменение рейса {number}", font=("Arial", 20)).pack(pady=10)

            self.train_date_entry = ctk.CTkEntry(self.root, placeholder_text="Дата отправления (гггг-мм-дд)")
            self.train_date_entry.insert(0, train.departure_date)
            self.train_date_entry.pack(pady=5)
            self.train_time_entry = ctk.CTkEntry(self.root, placeholder_text="Время отправления (чч:мм)")
            self.train_time_entry.insert(0, train.departure_time)
            self.train_time_entry.pack(pady=5)
            self.train_origin_entry = ctk.CTkEntry(self.root, placeholder_text="Место отправления")
            self.train_origin_entry.insert(0, train.origin)
            self.train_origin_entry.pack(pady=5)
            self.train_destination_entry = ctk.CTkEntry(self.root, placeholder_text="Место прибытия")
            self.train_destination_entry.insert(0, train.destination)
            self.train_destination_entry.pack(pady=5)
            self.train_seats_entry = ctk.CTkEntry(self.root, placeholder_text="Места")
            self.train_seats_entry.insert(0, train.seats)
            self.train_seats_entry.pack(pady=5)

            ctk.CTkButton(self.root, text="Сохранить", command=lambda: self.save_edited_train(train)).pack(pady=5)
            ctk.CTkButton(self.root, text="Назад", command=self.manage_trains).pack(pady=5)
        else:
            messagebox.showerror("Ошибка!", "Рейс не найден")

    def save_edited_train(self, train):
        train.departure_date = self.train_date_entry.get()
        train.departure_time = self.train_time_entry.get()
        train.origin = self.train_origin_entry.get()
        train.destination = self.train_destination_entry.get()

        try:
            train.seats = int(self.train_seats_entry.get())
            self.save_trains()
            messagebox.showinfo("Успешно!", "Поезд успешно обнавлен")
            self.manage_trains()
        except ValueError:
            messagebox.showerror("Ошибка!", "Место: должно быть число")

    def delete_train(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="Удалить рейс", font=("Arial", 20)).pack(pady=10)

        self.delete_train_number_entry = ctk.CTkEntry(self.root, placeholder_text="Номер рейса")
        self.delete_train_number_entry.pack(pady=5)
        ctk.CTkButton(self.root, text="Удалить", command=self.confirm_delete_train).pack(pady=5)
        ctk.CTkButton(self.root, text="Назад", command=self.manage_trains).pack(pady=5)

    def confirm_delete_train(self):
        number = self.delete_train_number_entry.get()
        train = next((t for t in self.trains if t.number == number), None)

        if train:
            self.trains.remove(train)
            self.save_trains()
            messagebox.showinfo("Успешно!", "Поезд успешно добавлен")
            self.manage_trains()
        else:
            messagebox.showerror("Ошибка!", "Поезд не найден")

    def build_user_dashboard(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text=f"Добро пожаловать, {self.current_user.username}!", font=("Arial", 20)).pack(pady=10)
        ctk.CTkButton(self.root, text="Купить билет", command=self.view_trains).pack(pady=5)
        ctk.CTkButton(self.root, text="Мои билеты", command=self.view_my_tickets).pack(pady=5)
        ctk.CTkButton(self.root, text="Информация о станции", command=self.information).pack(pady=5)
        ctk.CTkButton(self.root, text="Выход", command=self.build_login_screen).pack(pady=5)

    def book_ticket(self):
        train_number = self.train_booking_entry.get()
        train = next((t for t in self.trains if t.number == train_number), None)

        if not train:
            messagebox.showerror("Ошибка!", "Поезд не найден")
            return

        if train.seats <= 0:
            messagebox.showerror("Ошибка!", "Нет свободных мест")
            return

        train.seats -= 1
        self.save_trains()

        if train_number not in self.current_user.tickets:
            self.current_user.tickets.append(train_number)
            self.save_users()

        messagebox.showinfo("Успешно!", f"Билет забронирован на поезд {train.number}")
        self.view_trains()

    def return_ticket(self):
        ticket_number = self.ticket_return_entry.get()

        if ticket_number not in self.current_user.tickets:
            messagebox.showerror("Ошибка!", "Билет не найден в ваших покупках")
            return

        train = next((t for t in self.trains if t.number == ticket_number), None)
        if not train:
            messagebox.showerror("Ошибка!", "Поезд не найден")
            return

        train.seats += 1
        self.current_user.tickets.remove(ticket_number)
        self.save_trains()
        self.save_users()
        messagebox.showinfo("Успешно!", f"Билет на поезд {ticket_number} был возвращен")
        self.view_my_tickets()

    def information(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="Информация о станции:", font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(self.root, text="Станция: Сосновый бор", font=("Arial", 15)).pack(pady=10)
        ctk.CTkLabel(self.root, text="Количество платформ: 5", font=("Arial", 15)).pack(pady=10)
        ctk.CTkLabel(self.root, text="Город: Приреченск", font=("Arial", 15)).pack(pady=10)
        ctk.CTkLabel(self.root, text="Контактный телефон: 222-333-666 ", font=("Arial", 15)).pack(pady=10)
        ctk.CTkButton(self.root, text="Назад", command=self.build_user_dashboard).pack(pady=5)

    def view_trains(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="Возможные рейсы:", font=("Arial", 20)).pack(pady=10)

        for train in self.trains:
            train_info = f"Рейс {train.number}: {train.origin} - {train.destination}, Дата: {train.departure_date}, Время: {train.departure_time}, Места: {train.seats}"
            ctk.CTkLabel(self.root, text=train_info, font=("Arial", 12)).pack(pady=2)

        self.train_booking_entry = ctk.CTkEntry(self.root, placeholder_text="Введите номер рейса")
        self.train_booking_entry.pack(pady=5)
        ctk.CTkButton(self.root, text="Купить", command=self.book_ticket).pack(pady=5)
        ctk.CTkButton(self.root, text="Назад", command=self.build_user_dashboard).pack(pady=5)

    def view_my_tickets(self):
        self.clear_screen()
        ctk.CTkLabel(self.root, text="Мои билеты", font=("Arial", 20)).pack(pady=10)

        if not self.current_user.tickets:
            ctk.CTkLabel(self.root, text="No tickets booked.", font=("Arial", 12)).pack(pady=5)
        else:
            for ticket in self.current_user.tickets:
                ctk.CTkLabel(self.root, text=f"Рейс {ticket}", font=("Arial", 12)).pack(pady=2)

        self.ticket_return_entry = ctk.CTkEntry(self.root, placeholder_text="Введите номер рейса для возврата")
        self.ticket_return_entry.pack(pady=5)
        ctk.CTkButton(self.root, text="Вернуть билет", command=self.return_ticket).pack(pady=5)
        ctk.CTkButton(self.root, text="Назад", command=self.build_user_dashboard).pack(pady=5)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()