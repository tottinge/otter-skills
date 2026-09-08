from customer_name import customer_name


def invoice_heading(customer):
    return f"Bill to: {customer_name(customer['first'], customer['last'])}"
