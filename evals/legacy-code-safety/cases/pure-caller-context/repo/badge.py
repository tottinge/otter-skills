from customer_name import customer_name


def badge_text(registration):
    return customer_name(registration.get("first", ""), registration.get("last", "")).upper()
