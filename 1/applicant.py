import re

class Applicant:
    @staticmethod
    def validate_name(name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя - не пустая строка")

    @staticmethod
    def validate_address(address):
        if not isinstance(address, str):
            raise ValueError("Адрес - не пустая строка")

    @staticmethod
    def validate_phone(value):
        if not value.strip():
            raise ValueError("Телефон - не пустая строка.")
        if not re.match(r'^\+\d{1,3}\d{3}\d{3}\d{4}$', value):
            raise ValueError("Телефон должен быть формата +XXXXXXXXXXX.")
        return value

    @staticmethod
    def validate_profession(profession):
        if not isinstance(profession, str):
          raise ValueError("Профессия - не пустая стрка")
  
  def __init__(self, id, name, address, phone, profession):
    Applicant.validate_name(name)
    Applicant.validate_address(address)
    Applicant.validate_phone(phone)
    Applicant.validate_profession(profession)
    
    self._id = id
    self._name = name
    self._address = address
    self._phone = phone
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

  def get_phone(self):
    return self._phone

  def set_phone(self, phone):
    self._phone = phone

  def get_profession(self):
    return self._profession

  def set_profession(self, profession):
    self._profession = profession

  def __str__(self):
    return f"Applicant(ID ={self._id}, Имя ='{self._name}', Адрес ='{self._address}', Телефон ='{self._phone}', Профессия ='{self._profession}')"


try:
    applicant1 = Applicant(1, "Иван Иванович", "Пушкина 1", "+78888888888", "Кассир") #Всеправильно
    print(applicant1)
except ValueError as e:
    print(f"Ошибка создания Соискателя: {e}")

try:
    applicant2 = Applicant(2, "", "Пушкина 1", "+78888888888", "Кассир") #Неправильное имя
    print(applicant2)
except ValueError as e:
    print(f"Ошибка создания Соискателя: {e}")

try:
    applicant3 = Applicant(3, 123, "Пушкина 1", "+78888888888", "Кассир") #Неправильное имя
    print(applicant3)
except ValueError as e:
    print(f"Ошибка создания Соискателя: {e}")
