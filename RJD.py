
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class AuthApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Вход в систему")
        self.master.geometry("400x300")
        self.master.configure(bg="#FFFFFF")

        # Создание полей ввода для имени пользователя и пароля
        self.username_label = ctk.CTkLabel(master, text="Логин:")
        self.username_label.pack(pady=(20, 0))
        self.username_entry = ctk.CTkEntry(master)
        self.username_entry.pack(pady=(0, 10))

        self.password_label = ctk.CTkLabel(master, text="Пароль:")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = ctk.CTkEntry(master, show='*')
        self.password_entry.pack(pady=(0, 20))

        # Кнопки
        self.login_button = ctk.CTkButton(master, text="Войти", command=self.login)
        self.login_button.pack(pady=(0, 10))

        self.register_button = ctk.CTkButton(master, text="Зарегистрироваться", command=self.open_registration)
        self.register_button.pack(pady=(0, 10))

        self.exit_button = ctk.CTkButton(master, text="Выход", command=master.quit)
        self.exit_button.pack(pady=(0, 10))

        self.users = {}  # Хранение пользователей
        self.admin_credentials = {'admin': 'adminpassword'}  # Учетные данные администратора

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == password:
            self.open_main_menu(username)
        elif username in self.admin_credentials and self.admin_credentials[username] == password:
            self.open_admin_menu()
        else:
            ctk.CTkMessageBox.show_error("Ошибка", "Неверный логин или пароль")

    def open_registration(self):
        self.registration_window = ctk.CTkToplevel(self.master)
        self.registration_window.title("Регистрация")
        self.registration_window.geometry("400x300")
        self.registration_window.configure(bg="#FFFFFF")

        # Ввод данных для регистрации
        self.passport_label = ctk.CTkLabel(self.registration_window, text="Серия и номер паспорта:")
        self.passport_label.pack(pady=(20, 0))
        self.passport_entry = ctk.CTkEntry(self.registration_window)
        self.passport_entry.pack(pady=(0, 10))

        self.new_username_label = ctk.CTkLabel(self.registration_window, text="Придумайте логин:")
        self.new_username_label.pack(pady=(10, 0))
        self.new_username_entry = ctk.CTkEntry(self.registration_window)
        self.new_username_entry.pack(pady=(0, 10))

        self.new_password_label = ctk.CTkLabel(self.registration_window, text="Придумайте пароль:")
        self.new_password_label.pack(pady=(10, 0))
        self.new_password_entry = ctk.CTkEntry(self.registration_window, show='*')
        self.new_password_entry.pack(pady=(0, 20))

        self.register_confirm_button = ctk.CTkButton(self.registration_window, text="Зарегистрироваться", command=self.register)
        self.register_confirm_button.pack(pady=(0, 10))

    def register(self):
        passport = self.passport_entry.get()
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if username in self.users:
            ctk.CTkMessageBox.show_error("Ошибка", "Пользователь с таким логином уже существует")
            return

        self.users[username] = password
        ctk.CTkMessageBox.show_info("Успех", "Регистрация успешна")
        self.registration_window.destroy()

    def open_main_menu(self, username):
        self.master.withdraw()
        self.main_menu_window = ctk.CTkToplevel(self.master)
        self.main_menu_window.title("Главное меню")
        self.main_menu_window.geometry("400x300")
        self.main_menu_window.configure(bg="#FFFFFF")

        welcome_label = ctk.CTkLabel(self.main_menu_window, text=f"Добро пожаловать, {username}!")
        welcome_label.pack(pady=(20, 10))

        self.schedule_button = ctk.CTkButton(self.main_menu_window, text="Посмотреть расписание", command=self.view_schedule)
        self.schedule_button.pack(pady=(10, 10))

        self.buy_ticket_button = ctk.CTkButton(self.main_menu_window, text="Купить билет", command=self.buy_ticket)
        self.buy_ticket_button.pack(pady=(10, 10))

        self.check_price_button = ctk.CTkButton(self.main_menu_window, text="Узнать стоимость", command=self.check_price)
        self.check_price_button.pack(pady=(10, 10))

        self.logout_button = ctk.CTkButton(self.main_menu_window, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=(10, 10))

    def open_admin_menu(self):
        self.master.withdraw()
        self.admin_menu_window = ctk.CTkToplevel(self.master)
        self.admin_menu_window.title("Меню администратора")
        self.admin_menu_window.geometry("400x300")
        self.admin_menu_window.configure(bg="#FFFFFF")

        admin_label = ctk.CTkLabel(self.admin_menu_window, text="Меню администратора")
        admin_label.pack(pady=(20, 10))

        self.edit_schedule_button = ctk.CTkButton(self.admin_menu_window, text="Редактировать расписание", command=self.edit_schedule)
        self.edit_schedule_button.pack(pady=(10, 10))

        self.edit_price_button = ctk.CTkButton(self.admin_menu_window, text="Редактировать цены", command=self.edit_price)
        self.edit_price_button.pack(pady=(10, 10))

        self.logout_button = ctk.CTkButton(self.admin_menu_window, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=(10, 10))

    def logout(self):
        self.master.deiconify()
        if hasattr(self, 'main_menu_window'):
            self.main_menu_window.destroy()
        if hasattr(self, 'admin_menu_window'):
            self.admin_menu_window.destroy()

    def view_schedule(self):
        ctk.CTkMessageBox.show_info("Расписание", "Здесь будет расписание.")

    def buy_ticket(self):
        ctk.CTkMessageBox.show_info("Покупка билета", "Функция покупки билета еще в разработке.")

    def check_price(self):
        ctk.CTkMessageBox.show_info("Стоимость", "Здесь будет информация о стоимости.")

    def edit_schedule(self):
        ctk.CTkMessageBox.show_info("Редактирование расписания", "Функция редактирования расписания еще в разработке.")

    def edit_price(self):
        ctk.CTkMessageBox.show_info("Редактирование цен", "Функция редактирования цен еще в разработке.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = AuthApp(root)
    root.mainloop()
