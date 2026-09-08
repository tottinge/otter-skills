def parse_timeout(raw_value):
    if not raw_value.strip():
        return 0
    return int(raw_value)
