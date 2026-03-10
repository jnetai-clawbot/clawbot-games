#!/usr/bin/env python3
"""
ClawBot Security Tools
Password generator and file encryption utilities
"""

import os
import random
import string
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet

# Generate a key for encryption (save this!)
KEY_FILE = Path.home() / ".clawbot" / "encryption.key"

def generate_password(length=16, use_special=True):
    """Generate a secure random password"""
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def check_password_strength(password):
    """Check password strength"""
    score = 0
    
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
    
    strength = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"][score]
    return score, strength

def hash_password(password, salt=None):
    """Hash a password with SHA-256"""
    if not salt:
        salt = os.urandom(32)
    else:
        salt = salt.encode()
    
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.b64encode(salt + key).decode()

def encrypt_file(filename, key=None):
    """Encrypt a file"""
    if not key:
        if KEY_FILE.exists():
            with open(KEY_FILE) as f:
                key = f.read().strip()
        else:
            key = Fernet.generate_key()
            KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(KEY_FILE, 'w') as f:
                f.write(key.decode())
    
    f = Fernet(key)
    
    with open(filename, 'rb') as file:
        file_data = file.read()
    
    encrypted = f.encrypt(file_data)
    
    with open(filename + '.enc', 'wb') as file:
        file.write(encrypted)
    
    print(f"🔒 Encrypted: {filename} -> {filename}.enc")

def decrypt_file(filename, key=None):
    """Decrypt a file"""
    if not key:
        if KEY_FILE.exists():
            with open(KEY_FILE) as f:
                key = f.read().strip()
        else:
            print("❌ No encryption key found!")
            return
    
    f = Fernet(key.encode())
    
    with open(filename, 'rb') as file:
        encrypted = file.read()
    
    try:
        decrypted = f.decrypt(encrypted)
        
        output = filename.replace('.enc', '')
        with open(output, 'wb') as file:
            file.write(decrypted)
        
        print(f"🔓 Decrypted: {filename} -> {output}")
    except:
        print("❌ Decryption failed! Wrong key?")

def main():
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description='ClawBot Security Tools')
    parser.add_argument('command', choices=['password', 'strength', 'encrypt', 'decrypt'])
    parser.add_argument('--length', '-l', type=int, default=16, help='Password length')
    parser.add_argument('--file', '-f', help='File to encrypt/decrypt')
    parser.add_argument('--key', '-k', help='Encryption key')
    parser.add_argument('args', nargs='*', help='Password to check')
    
    args = parser.parse_args()
    
    if args.command == 'password':
        pwd = generate_password(args.length)
        print(f"🔑 Generated Password: {pwd}")
        
        score, strength = check_password_strength(pwd)
        print(f"   Strength: {strength} ({score}/6)")
    
    elif args.command == 'strength':
        if args.args:
            pwd = ' '.join(args.args)
            score, strength = check_password_strength(pwd)
            print(f"Password: {'*' * len(pwd)}")
            print(f"Strength: {strength} ({score}/6)")
        else:
            print("Usage: strength <password>")
    
    elif args.command == 'encrypt':
        if args.file:
            encrypt_file(args.file, args.key)
        else:
            print("Usage: encrypt --file <filename>")
    
    elif args.command == 'decrypt':
        if args.file:
            decrypt_file(args.file, args.key)
        else:
            print("Usage: decrypt --file <filename>")


if __name__ == "__main__":
    main()
