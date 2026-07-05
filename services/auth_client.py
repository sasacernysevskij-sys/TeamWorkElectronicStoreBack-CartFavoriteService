import requests

from config import AUTH_SERVICE_URL

# ---проверяет токен пользователя
def get_current_user(token: str):
    try:
        response = requests.get(
            f"{AUTH_SERVICE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if response.status_code != 200:
            return None

        return response.json().get("user")

    except requests.RequestException:
        return None