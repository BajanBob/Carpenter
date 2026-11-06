import base64
import hashlib
import json

import pytest

from carpenter.chat import ChatSession, jsonn_decrypt, jsonn_encrypt


def test_roundtrip():
    enc = jsonn_encrypt("hello world", "secret")
    assert jsonn_decrypt(enc, "secret") == "hello world"


def test_bad_checksum_raises_valueerror():
    data = json.loads(jsonn_encrypt("hi", "k"))
    data["checksum"] = "deadbeef"
    with pytest.raises(ValueError):
        jsonn_decrypt(json.dumps(data), "k")


def test_invalid_utf8_raises_valueerror_not_crash():
    # Craft a valid Jsonn message whose decrypted bytes are invalid UTF-8,
    # with a correct checksum, so decryption reaches the decode step.
    # Before the fix this raised UnicodeDecodeError; now it must be ValueError.
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


def test_chatsession_roundtrip():
    session = ChatSession("key123")
    embedded = session.send_message("meet at noon")
    sent = session.sent_messages[-1]
    out = session.receive_message(embedded, len(sent["encrypted"]), sent["position"])
    assert out == "meet at noon"
