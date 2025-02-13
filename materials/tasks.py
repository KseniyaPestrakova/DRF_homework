from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_update_course(user_email, course_name):
    send_mail(
        subject=f"Обновление материалов курса: {course_name}",
        message=f"Материалы курса {course_name} обновлены.",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
    )


@shared_task
def check_last_login_user():
    today = timezone.now()
    users = User.objects.filter(last_login__isnull=False)
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
