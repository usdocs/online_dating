from django.conf import settings
from django.core.mail import send_mail


def send_mail_match(liker, liking):
    send_mail(
        'Совпадение симпатии!',
        f'Вы понравились, {str(liker.username)}!'
        f'Почта участника: {str(liker.email)}',
        settings.DEFAULT_FROM_EMAIL,
        [liking.email],
    )
