from codes import normalize_code


def catalog_key(raw):
    return "item:" + normalize_code(raw)
