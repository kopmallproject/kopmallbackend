from accounts.models import User
from core.models import RefreshToken

def get_tokens(user: User | None = None) -> dict:
    if user is None:
        return {}

    refresh = RefreshToken.for_user(user)

    token: dict = {
        "access": str(refresh.access_token),  # type: ignore
        "refresh": str(refresh),
    }

    return token