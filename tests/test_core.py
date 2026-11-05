from carpenter.core import greeting


def test_greeting():
    assert greeting("Barbados") == "Hello, Barbados!"
    assert greeting("  ") == "Hello!"
    assert greeting(None) == "Hello!"
