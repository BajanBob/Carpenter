# carpenter/chat.py: Chat functionality with Jsonn encryption
"""Chat functionality with Jsonn encryption and white noise obfuscation."""
import json
import random
import string
import time
import hashlib
import base64


def generate_white_noise(length=100):
    """Generate white noise data to hide messages within."""
    # Generate random printable characters to act as white noise
    noise_chars = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(noise_chars) for _ in range(length))


def jsonn_encrypt(message, key="default"):
    """Encrypt a message using Jsonn algorithm (JSON-based encryption)."""
    # Create a simple hash-based key for encryption
    key_hash = hashlib.sha256(key.encode()).digest()

    # Convert message to bytes
    message_bytes = message.encode('utf-8')

    # XOR with key hash (repeating if necessary)
    encrypted_bytes = bytearray()
    for i, byte in enumerate(message_bytes):
        encrypted_bytes.append(byte ^ key_hash[i % len(key_hash)])

    # Base64 encode for safe transmission
    encrypted_message = base64.b64encode(encrypted_bytes).decode('utf-8')

    # Wrap in JSON structure
    json_structure = {
        "type": "jsonn_encrypted",
        "payload": encrypted_message,
        "timestamp": int(time.time()),
        "checksum": hashlib.md5(encrypted_message.encode()).hexdigest()[:8]
    }

    return json.dumps(json_structure)


def jsonn_decrypt(encrypted_json, key="default"):
    """Decrypt a Jsonn encrypted message."""
    # Parse the JSON
    try:
        data = json.loads(encrypted_json)
        if data.get("type") != "jsonn_encrypted":
            raise ValueError("Invalid Jsonn format")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

    # Verify checksum
    expected_checksum = hashlib.md5(data["payload"].encode()).hexdigest()[:8]
    if data.get("checksum") != expected_checksum:
        raise ValueError("Checksum mismatch")

    # Decode base64
    try:
        encrypted_bytes = base64.b64decode(data["payload"])
    except Exception:
        raise ValueError("Invalid base64 encoding")

    # Create key hash
    key_hash = hashlib.sha256(key.encode()).digest()

    # XOR with key hash to decrypt
    decrypted_bytes = bytearray()
    for i, byte in enumerate(encrypted_bytes):
        decrypted_bytes.append(byte ^ key_hash[i % len(key_hash)])

    # The bytes are only valid text when the key is right and the data is intact.
    # Raise a clean ValueError (like the other failure paths) instead of letting
    # UnicodeDecodeError escape, so callers can handle every bad input the same way.
    try:
        return decrypted_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Decryption failed (wrong key or corrupted data)")


def embed_in_white_noise(message, noise_length=256):
    """Embed a message within white noise for obfuscation."""
    noise = generate_white_noise(noise_length)
    # Embed message at a random position in the noise
    insert_pos = random.randint(0, noise_length - len(message) - 1) if len(message) < noise_length else 0
    embedded = noise[:insert_pos] + message + noise[insert_pos + len(message):]
    return embedded, insert_pos


def extract_from_white_noise(embedded_message, message_length, position):
    """Extract original message from white noise."""
    return embedded_message[position:position + message_length]


class ChatSession:
    """Represents a chat session with encryption and obfuscation."""

    def __init__(self, encryption_key="default"):
        self.encryption_key = encryption_key
        self.sent_messages = []
        self.received_messages = []

    def send_message(self, plaintext):
        """Send a message through the encrypted chat channel."""
        # Encrypt the message
        encrypted = jsonn_encrypt(plaintext, self.encryption_key)

        # Embed in white noise
        embedded, position = embed_in_white_noise(encrypted)

        # Store for reference
        self.sent_messages.append({
            "original": plaintext,
            "encrypted": encrypted,
            "embedded": embedded,
            "position": position,
            "timestamp": time.time()
        })

        return embedded

    def receive_message(self, embedded_message, original_length, position):
        """Receive and decrypt a message from the chat channel."""
        # Extract from white noise
        extracted = extract_from_white_noise(embedded_message, original_length, position)

        # Decrypt the message
        try:
            decrypted = jsonn_decrypt(extracted, self.encryption_key)

            # Store for reference
            self.received_messages.append({
                "decrypted": decrypted,
                "extracted": extracted,
                "timestamp": time.time()
            })

            return decrypted
        except ValueError as e:
            return f"Decryption failed: {str(e)}"
