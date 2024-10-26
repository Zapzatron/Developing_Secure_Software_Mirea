import hashlib

strings_to_hash = [
    "apple",
    "mmmmm",
    "testa",
    "zyzzx",
]

for string in strings_to_hash:
    encoded_string = string.encode()
    print(
        f"Строка: {string}\n"
        f"    SHA-256: {hashlib.sha256(encoded_string).hexdigest()}\n"
        f"    MD5: {hashlib.md5(encoded_string).hexdigest()}"
    )