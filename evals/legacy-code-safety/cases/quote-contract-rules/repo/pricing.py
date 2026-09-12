from offers import lookup


def quote(subtotal, customer, find_offer=lookup):
    if subtotal < 0:
        raise ValueError("negative subtotal")
    offer = find_offer(customer)
    discount = min(offer.rate, 0.25) if offer.eligible else 0
    return max(5, round(subtotal * (1 - discount), 2))
