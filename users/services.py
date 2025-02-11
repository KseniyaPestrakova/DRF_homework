import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создание продукта в stripe."""
    product = stripe.Product.create(name=course.name)
    return product


def create_stripe_price(amount, product):
    """Создание цены в stripe."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product,
    )


def create_stripe_sessions(price):
    """Создание сессии на оплату в stripe."""
    sessions = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return sessions.get("id"), sessions.get("url")
