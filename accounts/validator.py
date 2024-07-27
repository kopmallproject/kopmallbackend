import re

from accounts.models import User

def validate_password(password):
    
    message = "password should contain uppercase, lowercase, numbers and symbols"
    
    if len(password) < 8:
        raise ValueError("password should not be less than 8")
    
    if not re.search(r'[A-Z]', password):
        raise ValueError(message)
    if not re.search(r'[a-z]', password):
        raise ValueError(message)
    if not re.search(r'\d', password):
        raise ValueError(message)
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError(message)
    
    return password

def validate_email(email):
    user = User.objects.filter(email__iexact=email).exists()

    if user:
        raise ValueError("choose another email")
    return email