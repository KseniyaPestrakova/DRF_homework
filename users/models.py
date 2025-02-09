from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон", help_text="Укажите номер телефона"
    )
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    CASH = "cash"
    TRANSFER = "transfer"

    STATUS_CHOICES = [
        (CASH, "наличные"),
        (TRANSFER, "безналичные"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="course")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name="lesson")
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=12, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.course if self.course else self.lesson} - {self.payment_date} - {self.payment_amount}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_subscribe")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default='NULL', related_name="course_subscribe")

    def __str__(self):
        return f"Подписка на курс id{self.course} для пользователя id{self.user}"

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"
