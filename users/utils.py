from django.contrib.auth import get_user_model

User = get_user_model()


def is_email_exists(email: str) -> bool:
    """
    Helper method to check if the User email already exists.
    This can be used when you want to validate the email uniqueness.

    Parameters
    __________

    email : str
        Email which you want to query and check if it exists.

    Returns
    _______

    bool
        True if email already exists else it will return false.
    """

    user_filter = User.objects.filter(email=email.lower())

    if user_filter.exists():
        return True
    return False


def is_mobile_exists(mobile_number: str) -> bool:
    """
    Helper method to check if the User mobile number already exists.
    This can be used when you want to validate the mobile number uniqueness.

    Parameters
    __________

    mobile number : str
        mobile number which you want to query and check if it exists.

    Returns
    _______

    bool
        True if mobile number already exists else it will return false.
    """

    user_filter = User.objects.filter(mobile_number=mobile_number)

    if user_filter.exists():
        return True
    return False
