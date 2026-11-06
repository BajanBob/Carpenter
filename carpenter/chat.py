# carpenter/chat.py: Live bidirectional text chat with Jsonn encryption and white noise modulation.

import hashlib
import random
import struct
import time
from typing import Tuple


def jsonn_encrypt(message: str, key: str) -> Tuple[str, int]:
    """Encrypt a message using Jsonn encryption (MATLAB-based 256-bit encryption).
    
    Args:
        message: The plaintext message to encrypt
        key: The encryption key
        
    Returns:
        Tuple of (encrypted_message_hex, timestamp)
    """
    # Generate a 256-bit key from the provided key using SHA-256
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()
    
    # Convert message to bytes
    message_bytes = message.encode('utf-8')
    
    # XOR encryption with key cycling
    encrypted_bytes = bytearray()
    for i, byte in enumerate(message_bytes):
        key_byte = key_hash[i % len(key_hash)]
        encrypted_bytes.append(byte ^ key_byte)
    
    # Add timestamp for synchronization
    timestamp = int(time.time())
    
    return (encrypted_bytes.hex(), timestamp)


def jsonn_decrypt(encrypted_hex: str, key: str) -> str:
    """Decrypt a message using Jsonn encryption.
    
    Args:
        encrypted_hex: The hex-encoded encrypted message
        key: The encryption key
        
    Returns:
        The decrypted plaintext message
    """
    # Generate the same 256-bit key
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()
    
    # Convert hex back to bytes
    encrypted_bytes = bytes.fromhex(encrypted_hex)
    
    # XOR decryption with key cycling
    decrypted_bytes = bytearray()
    for i, byte in enumerate(encrypted_bytes):
        key_byte = key_hash[i % len(key_hash)]
        decrypted_bytes.append(byte ^ key_byte)
    
    return decrypted_bytes.decode('utf-8')


def add_white_noise(data: str, intensity: float = 0.1) -> str:
    """Add white noise to data to hide it in normal traffic.
    
    Args:
        data: The data to hide
        intensity: Noise intensity (0.0 to 1.0)
        
    Returns:
        Data with added white noise
    """
    # Convert to list for manipulation
    chars = list(data)
    
    # Add random whitespace characters based on intensity
    noisy_chars = []
    for char in chars:
        noisy_chars.append(char)
        # With probability equal to intensity, add a zero-width space
        if random.random() < intensity:
            noisy_chars.append('\u200B')  # Zero-width space
    
    return ''.join(noisy_chars)


def remove_white_noise(data: str) -> str:
    """Remove white noise from data.
    
    Args:
        data: The data with noise
        
    Returns:
        Clean data without noise
    """
    # Remove zero-width spaces
    return data.replace('\u200B', '')


def send_message(message: str, key: str) -> str:
    """Send an encrypted message with white noise modulation.
    
    Args:
        message: The plaintext message
        key: The encryption key
        
    Returns:
        The noisy encrypted message ready for transmission
    """
    # Encrypt the message
    encrypted, timestamp = jsonn_encrypt(message, key)
    
    # Add timestamp to encrypted data
    data_with_timestamp = f"{encrypted}:{timestamp}"
    
    # Add white noise
    noisy_data = add_white_noise(data_with_timestamp)
    
    return noisy_data


def receive_message(noisy_data: str, key: str) -> str:
    """Receive and decrypt a message with white noise modulation.
    
    Args:
        noisy_data: The received noisy data
        key: The decryption key
        
    Returns:
        The decrypted plaintext message
    """
    # Remove white noise
    clean_data = remove_white_noise(noisy_data)
    
    # Extract encrypted message and timestamp
    if ':' in clean_data:
        encrypted_part, timestamp_str = clean_data.rsplit(':', 1)
        try:
            timestamp = int(timestamp_str)
            # In a real implementation, we might verify timestamp freshness
        except ValueError:
            pass  # Ignore timestamp if not valid
    else:
        encrypted_part = clean_data
    
    # Decrypt the message
    decrypted_message = jsonn_decrypt(encrypted_part, key)
    
    return decrypted_message
