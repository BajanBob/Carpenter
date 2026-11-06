# tests/test_chat.py: Tests for chat functionality
"""Tests for the chat functionality with Jsonn encryption and white noise."""
import base64
import hashlib
import json

import pytest

from carpenter.chat import (
    ChatSession,
    embed_in_white_noise,
    extract_from_white_noise,
    generate_white_noise,
    jsonn_decrypt,
    jsonn_encrypt,
)


def test_jsonn_encryption_decryption():
    """Encrypt then decrypt returns the original message."""
    original_message = "Hello, this is a secret message!"
    key = "my_secret_key"
    encrypted = jsonn_encrypt(original_message, key)
    assert jsonn_decrypt(encrypted, key) == original_message


def test_jsonn_with_wrong_key():
    """Decrypting with the wrong key must never return the original message
    (it either returns something different, or is rejected with ValueError)."""
    original_message = "Secret information"
    encrypted = jsonn_encrypt(original_message, "correct_key")
    try:
        decrypted = jsonn_decrypt(encrypted, "wrong_key")
    except ValueError:
        return  # rejected outright - acceptable
    assert decrypted != original_message


def test_invalid_utf8_raises_valueerror_not_crash():
    """A valid Jsonn message whose decrypted bytes are not valid UTF-8 must
    raise ValueError, not an uncaught UnicodeDecodeError (regression test)."""
    key = "k"
    key_hash = hashlib.sha256(key.encode()).digest()
    bad = bytes([0xff, 0xfe])  # not valid UTF-8
    cipher = bytes(bad[i] ^ key_hash[i % len(key_hash)] for i in range(len(bad)))
    payload = base64.b64encode(cipher).decode()
    msg = json.dumps({
        "type": "jsonn_encrypted",
        "payload": payload,
        "timestamp": 0,
        "checksum": hashlib.md5(payload.encode()).hexdigest()[:8],
    })
    with pytest.raises(ValueError):
        jsonn_decrypt(msg, key)


def test_bad_checksum_raises_valueerror():
    """A tampered checksum is rejected."""
    data = json.loads(jsonn_encrypt("hi", "k"))
    data["checksum"] = "deadbeef"
    with pytest.raises(ValueError):
        jsonn_decrypt(json.dumps(data), "k")


def test_white_noise_generation():
    """White noise is the requested length and differs between calls."""
    noise1 = generate_white_noise(100)
    noise2 = generate_white_noise(100)
    assert len(noise1) == 100
    assert len(noise2) == 100
    assert noise1 != noise2  # very unlikely to be equal


def test_embedding_extraction():
    """Embedding a message in white noise and extracting it returns the message."""
    message = "Hidden message"
    noise_length = 100
    embedded, position = embed_in_white_noise(message, noise_length)
    extracted = extract_from_white_noise(embedded, len(message), position)
    assert len(embedded) == noise_length
    assert extracted == message


def test_chat_session():
    """A full send/receive round trip through a ChatSession."""
    session = ChatSession("shared_key")
    message = "Test message for chat session"
    embedded = session.send_message(message)
    sent_record = session.sent_messages[-1]
    message_length = len(sent_record["encrypted"])
    position = sent_record["position"]
    received = session.receive_message(embedded, message_length, position)
    assert received == message
    assert len(session.sent_messages) == 1
    assert len(session.received_messages) == 1


def test_jsonn_structure():
    """Jsonn produces a JSON object with the expected fields."""
    encrypted = jsonn_encrypt("Structured message")
    data = json.loads(encrypted)
    assert "type" in data
    assert "payload" in data
    assert "timestamp" in data
    assert "checksum" in data
    assert data["type"] == "jsonn_encrypted"
