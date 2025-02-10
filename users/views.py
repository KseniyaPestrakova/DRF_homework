from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.models import Payments, User, Subscribe, Course
from users.serializers import PaymentsSerializer, UserSerializer, SubscribeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from users.services import create_stripe_product, create_stripe_price, create_stripe_sessions


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentStripeCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save()

        if payment.payment_method == "transfer":

            payment.user = self.request.user

            product = create_stripe_product(payment.course)
            price = create_stripe_price(payment.payment_amount, product.id)

            session_id, payment_link = create_stripe_sessions(price)

            payment.session_id = session_id
            payment.link = payment_link
            payment.save()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method")
    ordering_fields = ("payment_date",)


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


@method_decorator(name="post", decorator=swagger_auto_schema(operation_description="Описание метода POST"))
class SubscribeAPIView(APIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")
        course = get_object_or_404(Course, id=course_id)

        subscribe, created = Subscribe.objects.get_or_create(user=user, course=course)

        if created:
            message = "Подписка добавлена"
        else:
            subscribe.delete()
            message = "Подписка удалена"

        return Response({"message": message})
