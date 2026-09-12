from dataclasses import dataclass


@dataclass(frozen=True)
class Offer:
    eligible: bool
    rate: float


def lookup(customer):
    # This adapter stands in for the account service; no live service is available.
    raise RuntimeError("account service unavailable")
