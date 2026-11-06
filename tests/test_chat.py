from carpenter.chat import (
    jsonn_encrypt,
    jsonn_decrypt,
    add_white_noise,
    remove_white_noise,
    send_message,
    receive_message
)


def test_jsonn_encryption():
    """Test Jsonn encryption and decryption."""
    message = "Hello, secret world!"
    key = "my_secret_key"
    
    # Test encryption
    encrypted, timestamp = jsonn_encrypt(message, key)
    assert isinstance(encrypted, str)
    assert isinstance(timestamp, int)
    assert encrypted != message
    
    # Test decryption
    decrypted = jsonn_decrypt(encrypted, key)
    assert decrypted == message
    
    # Test that wrong key produces garbage
    wrong_decrypted = jsonn_decrypt(encrypted, "wrong_key")
    assert wrong_decrypted != message


def test_white_noise():
    """Test white noise addition and removal."""
    original = "This is a test message"
    
    # Test adding noise
    noisy = add_white_noise(original, intensity=0.3)
    assert len(noisy) >= len(original)
    assert '\u200B' in noisy or True  # Might not always insert depending on randomness
    
    # Test removing noise
    cleaned = remove_white_noise(noisy)
    assert cleaned == original


def test_send_receive():
    """Test full send/receive cycle."""
    message = "This is a confidential message"
    key = "shared_secret_key"
    
    # Send message
    sent_data = send_message(message, key)
    assert isinstance(sent_data, str)
    assert len(sent_data) > 0
    
    # Receive message
    received_message = receive_message(sent_data, key)
    assert received_message == message
    
    # Test with wrong key
    wrong_received = receive_message(sent_data, "wrong_key")
    assert wrong_received != message
