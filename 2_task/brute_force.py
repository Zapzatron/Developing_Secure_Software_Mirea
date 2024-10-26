# Без многопоточного режима.
import hashlib
import itertools
import time


def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def brute_force(hashes, alphabet, string_length):
    start_time = time.time()
    temp_count = 0
    total_hashes = len(hashes)

    for password_tuple in itertools.product(alphabet, repeat=string_length):
        password = ''.join(password_tuple)
        md5 = md5_hash(password)
        sha256 = sha256_hash(password)

        if md5 in hashes:
            print(f"Пароль: {password}, MD5: {md5}")
            temp_count += 1
        elif sha256 in hashes:
            print(f"Пароль: {password}, SHA-256: {sha256}")
            temp_count += 1

        if temp_count == total_hashes:
            break

    end_time = time.time()
    print(f"Время выполнения: {round(end_time - start_time, 2)} секунд")


if __name__ == "__main__":
    hash_values = [
        "1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad",
        "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
        "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f",
        "7a68f09bd992671bb3b19a5e70b7827e"
    ]
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    password_length = 5

    brute_force(hash_values, ALPHABET, password_length)

    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 41.33 секунд
