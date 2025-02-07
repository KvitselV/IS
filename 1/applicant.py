import re
import json
class Applicant:
  def __init__(self, id, name, address, phone, profession):
    self._id = id
    self._name = self.validate_value(name, "name", is_required=True, only_letters=True)
    self._address = self.validate_value(address, "adress", is_required=True, only_letters=False)
    self._phone = self.validate_value(phone, "phone", is_required=True, only_letters=False, regex=r'^\+\d{1,3}\d{3}\d{3}\d{4}$')
    self._profession = self.validate_value(profession, "profession", is_required=True, only_letters=True)

    @classmethod
    def from_json(cls, json_str: str):
        try:

            data = json.loads(json_str)


            required_fields = [
                'id', 'name', 'address', 'profession', 'phone'
            ]

            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Не найдена строка: {field}")


            return cls(
                id=data['id'],
                name=data['name'],
                address=data['address'],
                profession=data['profession'],
                phone=data['phone']
            )

        except json.JSONDecodeError:
            raise ValueError("Не корректный формат")
        except Exception as e:
            raise ValueError(f"Ошибка создания объекта: {str(e)}")
    
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

  def __repr__(self):
    return f"Applicant(ID={self._id}, Имя='{self._name}')"

  def __eq__(self, other):
    if not isinstance(other, Applicant):
        return False
    return self._id == other._id

json_data = '''
    {
        "id": 1,
        "name": "Иванов Иван Иванович",
        "address": "Пушкина 1",
        "profession": "Инженер",
        "phone": "+79898983374"
    }
    '''

try:
    applicant = Applicant.from_json(json_data)
    print(applicant)
except ValueError as e:
    print(f"Ошибка: {e}")
