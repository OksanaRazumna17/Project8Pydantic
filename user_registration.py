from pydantic import BaseModel, EmailStr, field_validator, ValidationError
# Импортируем необходимые классы и функции из библиотеки Pydantic:
# - BaseModel: базовый класс для создания моделей данных.
# - EmailStr: тип данных для валидации строк в формате email.
# - field_validator: декоратор для создания пользовательских валидаторов в Pydantic V2.
# - ValidationError: класс исключений для обработки ошибок валидации.

from typing import Optional


# Импортируем Optional из библиотеки typing, который используется для указания необязательных полей.

class Address(BaseModel):
    # Создаем модель данных для адреса, которая наследуется от BaseModel.
    city: str
    # Поле 'city': строка, представляющая город.
    street: str
    # Поле 'street': строка, представляющая улицу.
    house_number: int

    # Поле 'house_number': целое число, представляющее номер дома.

    @field_validator('city')
    # Используем декоратор @field_validator для создания пользовательской валидации поля 'city'.
    def city_must_be_longer_than_two_characters(cls, v):
        # Метод для проверки длины строки 'city'.
        if len(v) < 2:
            # Если длина строки меньше 2 символов, выбрасывается ошибка.
            raise ValueError('City name must be at least 2 characters long')
        return v
        # Если валидация прошла успешно, возвращаем значение.

    @field_validator('street')
    # Декоратор для валидации поля 'street'.
    def street_must_be_longer_than_three_characters(cls, v):
        # Метод для проверки длины строки 'street'.
        if len(v) < 3:
            # Если длина строки меньше 3 символов, выбрасывается ошибка.
            raise ValueError('Street name must be at least 3 characters long')
        return v
        # Если валидация успешна, возвращаем значение.

    @field_validator('house_number')
    # Декоратор для валидации поля 'house_number'.
    def house_number_must_be_positive(cls, v):
        # Метод для проверки, что значение 'house_number' положительное.
        if v <= 0:
            # Если значение меньше или равно нулю, выбрасывается ошибка.
            raise ValueError('House number must be positive')
        return v
        # Если значение корректное, возвращаем его.


class User(BaseModel):
    # Создаем модель данных для пользователя, которая наследуется от BaseModel.
    name: str
    # Поле 'name': строка, представляющая имя пользователя.
    age: int
    # Поле 'age': целое число, представляющее возраст пользователя.
    email: EmailStr
    # Поле 'email': строка, представляющая email пользователя, проверяется через EmailStr.
    is_employed: bool
    # Поле 'is_employed': булево значение, указывающее на занятость пользователя.
    address: Address

    # Поле 'address': вложенная модель данных Address, представляющая адрес пользователя.

    @field_validator('name')
    # Декоратор для валидации поля 'name'.
    def name_must_be_alphabetic(cls, v):
        # Метод для проверки, что имя состоит только из букв.
        if not v.isalpha():
            # Если имя содержит не только буквы, выбрасывается ошибка.
            raise ValueError('Name must contain only alphabetic characters')
        if len(v) < 2:
            # Если длина имени меньше 2 символов, выбрасывается ошибка.
            raise ValueError('Name must be at least 2 characters long')
        return v
        # Если валидация успешна, возвращаем значение.

    @field_validator('age')
    # Декоратор для валидации поля 'age'.
    def age_must_be_valid(cls, v):
        # Метод для проверки, что возраст находится в пределах допустимого диапазона.
        if v < 0 or v > 120:
            # Если возраст меньше 0 или больше 120, выбрасывается ошибка.
            raise ValueError('Age must be between 0 and 120')
        return v
        # Если возраст корректен, возвращаем значение.

    @field_validator('is_employed')
    # Декоратор для валидации поля 'is_employed', с учетом других полей.
    def validate_age_and_employment(cls, v, info):
        # Метод для проверки соответствия возраста и статуса занятости.
        age = info.data.get('age')
        # Получаем текущее значение поля 'age' из объекта info.
        if age is not None and age < 18 and v:
            # Если возраст пользователя меньше 18, но он указан как занятый (employed), выбрасывается ошибка.
            raise ValueError('User cannot be employed if under 18 years old')
        return v
        # Если валидация успешна, возвращаем значение.


import json


# Импортируем модуль json для работы с JSON-строками.

def register_user(json_data: str) -> str:
    # Функция принимает JSON строку, десериализует её в объект Pydantic, валидирует и возвращает обратно в JSON.
    try:
        user = User.parse_raw(json_data)
        # Десериализация JSON строки в объект User с помощью метода parse_raw.
        return user.json()
        # Сериализация объекта обратно в JSON и возвращение его.
    except ValidationError as e:
        # Если при валидации возникают ошибки, они перехватываются здесь.
        return str(e)
        # Возвращаем строку с описанием ошибок.


if __name__ == "__main__":
    # Если этот файл запускается как основной (а не импортируется как модуль), выполняется следующий код.

    # Успешная регистрация
    json_string_valid = '''
    {
        "name": "Alice",
        "age": 25,
        "email": "alice@example.com",
        "is_employed": true,
        "address": {
            "city": "New York",
            "street": "Main Street",
            "house_number": 123
        }
    }
    '''
    # Пример JSON строки с правильными данными для успешной валидации.

    # Неправильное имя и возраст
    json_string_invalid = '''
    {
        "name": "A1ice",
        "age": 17,
        "email": "alice@example.com",
        "is_employed": true,
        "address": {
            "city": "N",
            "street": "M",
            "house_number": 0
        }
    }
    '''
    # Пример JSON строки с некорректными данными, чтобы проверить обработку ошибок.

    print("Valid user registration:")
    # Выводим заголовок для теста с валидными данными.
    print(register_user(json_string_valid))
    # Печатаем результат работы функции register_user с валидными данными.

    print("\nInvalid user registration:")
    # Выводим заголовок для теста с невалидными данными.
    print(register_user(json_string_invalid))
    # Печатаем результат работы функции register_user с невалидными данными.
