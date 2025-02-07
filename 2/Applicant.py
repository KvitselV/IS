import yaml
import os
import json
import psycopg2
import re


class Applicant:
    @staticmethod
    def validate(field_name, field_value, expected_type):
        if not isinstance(field_value, expected_type):
            print(f"Поле '{field_name}' должно быть типа {expected_type}.")
            return False
        if expected_type is str and not field_value:
            print(f"Поле '{field_name}' не может быть пустым.")
            return False
        if expected_type is str and field_name == "Имя":
            if not re.fullmatch(r"[А-Яа-яЁё]+\s[А-Яа-яЁё]+", field_value):
                print(f"Поле '{field_name}' должно содержать имя и фамилию.")
                return False
        if expected_type is str and field_name == "Профессия" and not field_value.isalpha():
            print(f"Поле '{field_name}' должно содержать только буквы.")
            return False
        if expected_type is str and field_name == "Телефон" and not re.match(r"^\+\d+$", field_value):
            print(f"Поле '{field_name}' должно начинаться с '+' и содержать только цифры.")
            return False
        return True

    def __init__(self, id, name, address, phone, profession):
        self._id = id
        if not Applicant.validate("Имя", name, str):
            raise ValueError("Некорректные данные")
        self._name = name
        if not Applicant.validate("Адрес", address, str):
            raise ValueError("Некорректные данные")
        self._address = address
        if not Applicant.validate("Телефон", phone, str):
            raise ValueError("Некорректные данные")
        self._phone = phone
        if not Applicant.validate("Профессия", profession, str):
            raise ValueError("Некорректные данные")
        self._profession = profession

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_address(self):
        return self._address

    def set_address(self, address):
        self._address = address

    def set_phone(self, phone):
        self._phone = phone

    def get_phone(self):
        return self._phone

    def get_profession(self):
        return self._profession

    def set_profession(self, profession):
        self._profession = profession

    def __str__(self):
        return (f"Applicant(ID={self._id},"
                f" Имя='{self._name}',"
                f" Адрес='{self._address}',"
                f" Телефон='{self._phone}',"
                f" Профессия= '{self._profession}')")

    def short_version(self):
        return f"Applicant ID: {self._id}, Имя: {self._name}"

    def __eq__(self, other):
        if not isinstance(other, Applicant):
            return False
        return self._id == other._id


class ApplicantShort:
    def __init__(self, applicant):
        if not isinstance(applicant, Applicant):
            raise TypeError("Аргумент должен быть объектом класса Applicant.")
        self.id = applicant.get_id()
        name_parts = applicant.get_name().split()
        if len(name_parts) >= 2:
            self.name = name_parts[-1][0] + ". " + name_parts[0]
        else:
            self.name = applicant.get_name()
        self.phone = applicant.get_phone()

    def __str__(self):
        return f"ApplicantShort(ID={self.id}, Имя={self.name}, Телефон={self.phone})"


class ApplicantRep:
    def __init__(self, filepath=""):
        self.filepath = filepath
        self.applicants = []
        self.next_id = 1
        if os.path.exists(self.filepath):
            self.load_data()

    def load_data(self):
        pass

    def save_data(self):
        pass

    def get_all_applicants(self):
        return self.applicants

    def add_applicant(self, name, address, phone, profession):
        new_applicant = Applicant(self.next_id, name, address, phone, profession)
        self.applicants.append(new_applicant)
        self.next_id += 1
        self.save_data()
        return True

    def delete_applicant(self, applicant_id):
        self.applicants = [b for b in self.applicants if b.get_id() != applicant_id]
        self.save_data()
        return True

    def get_applicant_by_id(self, applicant_id):
        for applicant in self.applicants:
            if applicant.get_id() == applicant_id:
                return applicant
        return None

    def get_k_n_short_list(self, k, n):
        return [ApplicantShort(b) for b in self.applicants[k - 1:k + n - 1]]

    def sort_by_field(self, field):
        try:
            self.applicants.sort(key=lambda x: getattr(x, f"get_{field.lower()}")())
        except AttributeError:
            print(f"Поле '{field}' не найдено или у него нет геттера.")

    def get_count(self):
        return len(self.applicants)

    def replace_applicant(self, applicant_id, name, address, phone, profession):
        for i, applicant in enumerate(self.applicants):
            if applicant.get_id() == applicant_id:
                self.applicants[i] = Applicant(applicant_id, name, address, phone, profession)
                self.save_data()
                return True
        return False


class ApplicantRepJSON(ApplicantRep):
    def __init__(self, filepath="applicants.json"):
        super().__init__(filepath)

    def load_data(self):
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                for item in data:
                    self.applicants.append(Applicant(*item.values()))
                self.next_id = max(b.get_id() for b in self.applicants) + 1 if self.applicants else 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при загрузке из JSON: {e}")

    def save_data(self):
        try:
            data = [vars(b) for b in self.applicants]
            with open(self.filepath, "w") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при сохранении в JSON: {e}")


class ApplicantRepYAML(ApplicantRep):
    def __init__(self, filepath="applicants.yaml"):
        super().__init__(filepath)

    def load_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data:
                    for applicant_data in data:
                        self.applicants.append(Applicant(*applicant_data.values()))
                    self.next_id = max(b.get_id() for b in self.applicants) + 1 if self.applicants else 1
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при загрузке из YAML: {e}")

    def save_data(self):
        try:
            data = [vars(b) for b in self.applicants]
            with open(self.filepath, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Ошибка при сохранении в YAML: {e}")


class DatabaseConnector:
    __instance = None

    @staticmethod
    def get_instance(host, user, password, database, port=5432):
        if DatabaseConnector.__instance is None:
            DatabaseConnector(host, user, password, database, port)
        return DatabaseConnector.__instance

    def __init__(self, host, user, password, database, port=5432):
        if DatabaseConnector.__instance is not None:
            raise Exception("Это паттерн 'Одиночка'")
        else:
            DatabaseConnector.__instance = self
            self.connection = None
            self.cursor = None
            try:
                self.connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=port
                )
                self.cursor = self.connection.cursor()
            except psycopg2.Error as e:
                print(f"Ошибка подключения к базе данных PostgreSQL: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor
        except psycopg2.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()


class ApplicantRepDB:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def initialize_db(self):
        cursor = self.db_connector.execute_query("""
        CREATE TABLE IF NOT EXISTS Applicants (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL CHECK (Name ~* '^[а-яА-Яa-zA-Z\\s]+$'),
    Address TEXT NOT NULL,
    Phone VARCHAR(20) NOT NULL UNIQUE CHECK (Phone ~* '^\\+\\d+$'),
    profession TEXT NOT NULL CHECK (profession ~* '^[а-яА-Яa-zA-Z\\s]+$')
        );
        """)
        if cursor:
            print("База данных PostgreSQL и таблица 'Applicants' успешно созданы.")

    def get_applicant_by_id(self, applicant_id):
        cursor = self.db_connector.execute_query("SELECT * FROM Applicants WHERE ID = %s", (applicant_id,))
        if cursor:
            result = cursor.fetchone()
            if result:
                return Applicant(*result)
            else:
                return None
        return None

    def get_all_applicants(self):
        cursor = self.db_connector.execute_query("SELECT ID, Name, Address, Phone, profession FROM Applicants")
        if cursor:
            results = cursor.fetchall()
            return [Applicant(row[0], row[1], row[2], row[3], row[4]) for row in results]
        return []

    def add_applicant(self, applicant: Applicant):
        if not isinstance(applicant, Applicant):
            raise TypeError("Аргумент должен быть объектом класса Applicant.")
        query = """INSERT INTO Applicants (Name, Address, Phone, profession) 
                  VALUES (%s, %s, %s, %s) RETURNING ID;"""
        cursor = self.db_connector.execute_query(query, (applicant.get_name(),
                                                         applicant.get_address(),
                                                         applicant.get_phone(),
                                                         applicant.get_profession()))
        if cursor:
            result = cursor.fetchone()
            applicant.set_id(result[0])
            return applicant
        return None

    def replace_applicant(self, applicant: Applicant):
        if not isinstance(applicant, Applicant):
            raise TypeError("Аргумент должен быть объектом класса Applicant.")
        query = """UPDATE Applicants 
                  SET Name = %s, Address = %s, Phone = %s, profession = %s 
                  WHERE ID = %s"""
        cursor = self.db_connector.execute_query(query, (applicant.get_name(),
                                                         applicant.get_address(),
                                                         applicant.get_phone(),
                                                         applicant.get_profession(),
                                                         applicant.get_id()))
        if cursor and cursor.rowcount > 0:
            print("Данные Соискателя успешно обновлены.")
        else:
            print("Соискатель с таким ID не найден или данные не изменены.")

    def delete_applicant(self, applicant_id):
        try:
            cursor = self.db_connector.execute_query(
                "SELECT ID, Name, Address, Phone, profession FROM Applicants WHERE ID > %s", (applicant_id,))
            if cursor is None:
                return False
            applicants_to_update = cursor.fetchall()

            cursor = self.db_connector.execute_query("DELETE FROM Applicants WHERE ID = %s", (applicant_id,))
            if cursor is None or cursor.rowcount == 0:
                print("Соискатель с таким ID не найден")
                return False

            for i, applicant_data in enumerate(applicants_to_update):
                new_id = applicant_data[0] - 1
                update_query = """UPDATE Applicants SET ID = %s WHERE ID = %s"""
                self.db_connector.execute_query(update_query, (new_id, applicant_data[0]))

            return True
        except Exception as e:
            print(f"Ошибка при удалении Соискателя: {e}")
            return False

    def get_count(self):
        cursor = self.db_connector.execute_query("SELECT COUNT(*) FROM Applicants")
        if cursor:
            result = cursor.fetchone()
            return result[0] if result else 0
        return 0

    def get_k_n_short_list(self, k, n):
        offset = k - 1
        limit = n
        cursor = self.db_connector.execute_query(
            "SELECT ID, Name, Address, Phone, profession FROM Applicants LIMIT %s OFFSET %s", (limit, offset)
        )
        if cursor:
            results = cursor.fetchall()
            return [ApplicantShort(Applicant(*row)) for row in results]
        return []


class ApplicantRepDBAdapter(ApplicantRep):
    def __init__(self, db_connector):
        super().__init__()
        self.db_rep = ApplicantRepDB(db_connector)
        self.applicants = self.db_rep.get_all_applicants()
        self.next_id = self.db_rep.get_count() + 1 if self.db_rep.get_count() > 0 else 1

    def add_applicant(self, name, address, phone, profession):
        try:
            new_applicant = Applicant(self.next_id, name, address, phone, profession)
            added_applicant = self.db_rep.add_applicant(new_applicant)
            if added_applicant:
                self.applicants.append(added_applicant)
                self.next_id = self.db_rep.get_count() + 1
                return True
            return False
        except (psycopg2.Error, ValueError) as e:
            print(f"Ошибка при добавлении Соискателя: {e}")
            return False

    def delete_applicant(self, applicant_id):
        result = self.db_rep.delete_applicant(applicant_id)
        self.applicants = self.db_rep.get_all_applicants()
        self.next_id = self.db_rep.get_count() + 1 if self.db_rep.get_count() > 0 else 1
        return result

    def get_applicant_by_id(self, applicant_id):
        applicant_data = self.db_rep.get_applicant_by_id(applicant_id)
        return applicant_data

    def get_all_applicants(self):
        return self.db_rep.get_all_applicants()

    def get_k_n_short_list(self, k, n):
        short_list_data = self.db_rep.get_k_n_short_list(k, n)
        return short_list_data

    def sort_by_field(self, field):
        applicants = self.get_all_applicants()
        try:
            applicants.sort(key=lambda x: getattr(x, f"_{field}"))
            self.applicants = applicants
        except AttributeError:
            print(f"Поле '{field}' не найдено.")

    def replace_applicant(self, applicant_id, name, address, phone, profession):
        applicant = self.get_applicant_by_id(applicant_id)
        if applicant:
            applicant.set_name(name)
            applicant.set_address(address)
            applicant.set_phone(phone)
            applicant.set_profession(profession)
            self.db_rep.replace_applicant(applicant)
            self.applicants = self.db_rep.get_all_applicants()
            print("Данные Соискателя изменены")
        else:
            print("Соискатель не найден")

    def get_count(self):
        return self.db_rep.get_count()

    def save_data(self):
        pass


def run_operations(applicant_rep):
    applicants = applicant_rep.get_all_applicants()
    while True:
        print("\nМеню:")
        print("1. Вывести всех Соискателей")
        print("2. Добавить Соискателя")
        print("3. Удалить Соискателя")
        print("4. Изменить данные Соискателя")
        print("5. Найти Соискателя по ID")
        print("6. Получить k-n короткий список")
        print("7. Вывести кол-во Соискателей")
        print("8. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                print("\nВсе Соискатели:")
                for applicant in applicants:
                    print(applicant)
            elif choice == "2":
                while True:
                    try:
                        name = input("Введите имя и фамилию: ")
                        address = input("Введите адрес: ")
                        phone = input("Введите телефон (начинающийся с +): ")
                        profession = input("Введите Профессию: ")
                        break
                    except ValueError as e:
                        print(f"Ошибка валидации: {e}")

                if applicant_rep.add_applicant(name, address, phone, profession):
                    applicants = applicant_rep.get_all_applicants()
                    print("Соискатель добавлен")
                else:
                    print("Ошибка при добавлении Соискателя")
            elif choice == "3":
                applicant_id = int(input("Введите ID Соискателя для удаления: "))
                if applicant_rep.delete_applicant(applicant_id):
                    applicants = applicant_rep.get_all_applicants()
                    print("Соискатель удален")
                else:
                    print("Соискатель не найден или ошибка при удалении")
            elif choice == "4":
                applicant_id = int(input("Введите ID Соискателя для изменения: "))
                applicant = applicant_rep.get_applicant_by_id(applicant_id)
                if applicant:
                    name = input(f"Новое имя ({applicant.get_name()}): ") or applicant.get_name()
                    address = input(f"Новый адрес ({applicant.get_address()}): ") or applicant.get_address()
                    phone = input(f"Новый телефон ({applicant.get_phone()}): ") or applicant.get_phone()
                    profession = input(f"Новая Профессия ({applicant.get_profession()}): ") or applicant.get_profession()
                    applicant_rep.replace_applicant(applicant_id, name, address, phone, profession)
                    applicants = applicant_rep.get_all_applicants()
                    print("Данные Соискателя изменены")
                else:
                    print("Соискатель не найден")
            elif choice == "5":
                applicant_id = int(input("Введите ID Соискателя: "))
                applicant = applicant_rep.get_applicant_by_id(applicant_id)
                if applicant:
                    print("\nНайденный Соискатель:", applicant)
                else:
                    print("Соискатель не найден.")
            elif choice == "6":
                k = int(input("Введите начальный элемент (k): "))
                n = int(input("Введите количество элементов (n): "))
                short_list = applicant_rep.get_k_n_short_list(k, n)
                print("\nКраткая информация о Соискателях:")
                for applicant in short_list:
                    print(str(applicant))
            elif choice == "7":
                count = applicant_rep.get_count()
                print(f"Количество Соискателей: {count}")
            elif choice == "8":
                print("Выход")
                break
            else:
                print("Неверный выбор")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def run_prog():
    storage_type = input("Выберите тип хранилища (db, json, yaml): ")
    db_connector = None
    try:
        if storage_type == "db":
            host = 'localhost'
            user = 'postgres'
            password = 'vadimb'
            database = 'Applicants'
            db_connector = DatabaseConnector.get_instance(host, user, password, database)
            if db_connector.connection is None:
                print("Ошибка подключения к базе данных.")
                return
            applicant_rep = ApplicantRepDBAdapter(db_connector)
            applicant_rep.db_rep.initialize_db()
        elif storage_type == "json":
            applicant_rep = ApplicantRepJSON()
        elif storage_type == "yaml":
            applicant_rep = ApplicantRepYAML()
        else:
            raise ValueError("Неподдерживаемый тип хранилища данных")
        run_operations(applicant_rep)
        if storage_type == "db" and db_connector:
            db_connector.close()
    except ValueError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    run_prog()
