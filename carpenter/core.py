"""Carpenter's logic, kept free of any user-interface code so it can be tested on every platform."""


def greeting(name):
    name = (name or "").strip()
    return f"Hello, {name}!" if name else "Hello!"
