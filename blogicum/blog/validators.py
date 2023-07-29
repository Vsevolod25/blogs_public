from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone


def pub_date(pub_date: datetime) -> None:
    if pub_date < timezone.now():
        raise ValidationError(
            f'Ожидается время после { datetime.now() }'
        )
