# tests/test_chat.py: Tests for chat functionality
"""Tests for the chat functionality with Jsonn encryption."""
import json
from carpenter.chat import (
    jsonn_encrypt, 
    jsonn_decrypt, 
    generate_white_noise, 
    embed_in_white_noise, 
    extract_from_white_noise,
    ChatSession
)


def test_jsonn_encryption_decryption():
    """Test Jsonn encryption and decryption."""
    original_message = "Hello, this is a secret message!"
    key = "my_secret_key"
    
    # Encrypt the message
    encrypted = jsonn_encrypt(original_message, key)
    
    # Decrypt the message
    decrypted = jsonn_decrypt(encrypted, key)
    
    assert decrypted == original_message


def test_jsonn_with_wrong_key():
    """Test Jsonn decryption with wrong key produces garbage."""
    original_message = "Secret information"
    key1 = "correct_key"
    key2 = "wrong_key"
    
    # Encrypt with key1
    encrypted = jsonn_encrypt(original_message, key1)
    
    # Decrypt with key2 should produce different result
    decrypted = jsonn_decrypt(encrypted, key2)
    
    assert decrypted != original_message


def test_white_noise_generation():
    """Test white noise generation."""
    noise1 = generate_white_noise(100)
    noise2 = generate_white_noise(100)
    
    assert len(noise1) == 100
    assert len(noise2) == 100
    assert noise1 != noise2  # Very unlikely to be equal


def test_embedding_extraction():
    """Test embedding message in white noise and extracting it."""
    message = "Hidden message"
    noise_length = 100
    
    # Embed message
    embedded, position = embed_in_white_noise(message, noise_length)
    
    # Extract message
    extracted = extract_from_white_noise(embedded, len(message), position)
    
    assert len(embedded) == noise_length
    assert extracted == message


def test_chat_session():
    """Test complete chat session."""
    session = ChatSession("shared_key")
    message = "Test message for chat session"
    
    # Send message
    embedded = session.send_message(message)
    
    # Get the length and position for extraction
    sent_record = session.sent_messages[-1]
    message_length = len(sent_record["encrypted"])
    position = sent_record["position"]
    
    # Receive message
    received = session.receive_message(embedded, message_length, position)
    
    assert received == message
    assert len(session.sent_messages) == 1
    assert len(session.received_messages) == 1


def test_jsonn_structure():
    """Test that Jsonn produces proper JSON structure."""
    message = "Structured message"
    encrypted = jsonn_encrypt(message)
    
    # Should be valid JSON
    data = json.loads(encrypted)
    
    # Check required fields
    assert "type" in data
    assert "payload" in data
    assert "timestamp" in data
    assert "checksum" in data
    assert data["type"] == "jsonn_encrypted"
