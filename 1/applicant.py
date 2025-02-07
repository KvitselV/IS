import re

class Applicant:
  def __init__(self, id, name, address, phone, profession):
    self._id = id
    self._name = self.validate_value(name, "name", is_required=True, only_letters=True)
    self._address = self.validate_value(address, "adress", is_required=True, only_letters=False)
    self._phone = self.validate_value(phone, "phone", is_required=True, only_letters=False, regex=r'^\+\d{1,3}\d{3}\d{3}\d{4}$')
    self._profession = self.validate_value(profession, "profession", is_required=True, only_letters=True)

    @staticmethod
    def validate_value(value, field_name, is_required=True, only_letters=False, regex=None):

        if is_required and not value.strip():
            raise ValueError(f"{field_name} Не может быть пустой")

        if only_letters and not value.replace(" ", "").isalpha():
            raise ValueError(f"{field_name} Не может содержать цифр")

        if regex and not re.match(regex, value):
            raise ValueError(f"{field_name} Неверный формат: {regex}")

        return value  

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
    applicant3 = Applicant(3, "123", "Пушкина 1", "+78888888888", "Кассир") #Неправильное имя
    print(applicant3)
except ValueError as e:
    print(f"Ошибка создания Соискателя: {e}")
