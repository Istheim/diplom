import string
from django.utils.crypto import get_random_string


def generate_digit_code() -> str:
    """
     При вызове генерирует строку из 4 случайных цифр. Возвращает результат в виде строки
    """
    return get_random_string(length=4, allowed_chars=string.digits)


def generate_invite_code() -> str:
    """
    При вызове генерирует строку из 6 случайных чисел и букв в нижнем регистре.
    Возвращает результат в виде строки
    """

    return get_random_string(length=6, allowed_chars=string.ascii_lowercase + string.digits)
