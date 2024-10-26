import threading
import hashlib
import time
import itertools


def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()


def sha256_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def brute_force(start, end, hashes, strings):
    for i in range(start, end):
        password = strings[i]

        md5 = md5_hash(password)
        sha256 = sha256_hash(password)

        if md5 in hashes:
            print(f"Пароль: {password}, MD5: {md5}")
        elif sha256 in hashes:
            print(f"Пароль: {password}, SHA-256: {sha256}")


def run_threaded_brute_force(num_threads, hashes, alphabet, string_length):
    strings = ["".join(tuple_string) for tuple_string in itertools.product(alphabet, repeat=string_length)]

    threads = []
    start_time = time.time()

    chunk_size = len(strings) // num_threads
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_threads - 1 else len(strings)
        thread = threading.Thread(target=brute_force, args=(start, end, hashes, strings))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Время выполнения: {round(end_time - start_time, 2)} секунд")


if __name__ == "__main__":
    NUM_THREADS = int(input("Введите количество потоков: "))
    # NUM_THREADS = 1
    hash_values = [
        "1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad",
        "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
        "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f",
        "7a68f09bd992671bb3b19a5e70b7827e"
    ]
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    password_length = 5

    run_threaded_brute_force(NUM_THREADS, hash_values, ALPHABET, password_length)

    # Введите количество потоков: 1
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 39.47 секунд

    # Введите количество потоков: 2
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 39.78 секунд

    # Введите количество потоков: 3
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 38.64 секунд

    # Введите количество потоков: 4
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 39.81 секунд
