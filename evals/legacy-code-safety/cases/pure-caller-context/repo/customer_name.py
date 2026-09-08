def customer_name(first_name, last_name):
    parts = [part.strip().title() for part in (first_name, last_name) if part.strip()]
    return " ".join(parts) or "Guest"
