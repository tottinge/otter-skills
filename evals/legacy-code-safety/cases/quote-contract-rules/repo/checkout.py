from pricing import quote


def checkout_total(basket, customer):
    # Checkout displays a currency amount, including the minimum charge for empty baskets.
    return f"{quote(sum(basket), customer):.2f}"
