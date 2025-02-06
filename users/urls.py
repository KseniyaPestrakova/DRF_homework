from users.apps import UsersConfig
from django.urls import path
from users.views import PaymentsCreateAPIView, PaymentsListAPIView, PaymentsRetrieveAPIView, \
    PaymentsUpdateAPIView, PaymentsDestroyAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments-create'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path('payments/<int:pk>/', PaymentsRetrieveAPIView.as_view(), name='payments-get'),
    path('payments/update/<int:pk>/', PaymentsUpdateAPIView.as_view(), name='payments-update'),
    path('payments/delete/<int:pk>/', PaymentsDestroyAPIView.as_view(), name='payments-delete'),
]
