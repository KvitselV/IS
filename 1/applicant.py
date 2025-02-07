class Applicant:
  def __init__(self, id, name, address, phone, profession):
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


applicant1 = Applicant(1, "Иван Иванович", "Пушкина 1", "+777777777", "Кассир")
print(applicant1)
