import re

from django.core.exceptions import ValidationError


def validate_username(username):
    """Проверить username на допустимость."""

    pattern = re.compile(r'^[\w.@+-]+\Z')

    if username.lower() == "me":
        raise ValidationError(
            message="Использовать имя 'me' в качестве username запрещено. "
        )
    if not pattern.findall(username):
        raise ValidationError(
            "Username содержит некорректные символы."
        )
