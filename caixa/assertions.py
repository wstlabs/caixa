
def assert_instance(obj: object, cls: type) -> None:
    if not isinstance(obj, cls):
        raise TypeError(f"expected an instance of type '{cls}', got '{type(obj)}'")

