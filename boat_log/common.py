

def dict_from_attr_list(items: list, obj: object) -> dict:
    attrs = {}
    for item in items:
        if getattr(obj, item, False):
            attrs[item] = getattr(obj, item)
    return attrs
