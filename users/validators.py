import re
from rest_framework import serializers


def password_regex_validator(password: str) -> None:
    """To check if the password is in proper format using regex.

    Parameters
    __________

    password: str
        password which you want to chakc the format of.

    """

    pattern = re.compile(
        r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')

    match = re.fullmatch(pattern, password)

    if not match:
        raise serializers.ValidationError("""
            Password should contain:Uppercase, Lowercase, and
            Numerical Character.""")
