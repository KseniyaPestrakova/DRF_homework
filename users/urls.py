from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentsCreateAPIView,
    PaymentsDestroyAPIView,
    PaymentsListAPIView,
    PaymentsRetrieveAPIView,
    PaymentStripeCreateAPIView,
    PaymentsUpdateAPIView,
    SubscribeAPIView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UsersRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("payments/create/", PaymentsCreateAPIView.as_view(), name="payments-create"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments-list"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payments-get"),
    path("payments/update/<int:pk>/", PaymentsUpdateAPIView.as_view(), name="payments-update"),
    path("payments/delete/<int:pk>/", PaymentsDestroyAPIView.as_view(), name="payments-delete"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("<int:pk>/", UsersRetrieveAPIView.as_view(), name="user-get"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user-delete"),
    path("subscribe/", SubscribeAPIView.as_view(), name="subscribe"),
    path("payments/stripe/", PaymentStripeCreateAPIView.as_view(), name="payments-stripe"),
]
