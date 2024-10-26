import multiprocessing
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


def run_multiprocess_brute_force(num_processes, hashes, alphabet, string_length):
    strings = ["".join(tuple_string) for tuple_string in itertools.product(alphabet, repeat=string_length)]

    processes = []
    start_time = time.time()

    chunk_size = len(strings) // num_processes
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_processes - 1 else len(strings)
        process = multiprocessing.Process(target=brute_force, args=(start, end, hashes, strings))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Время выполнения: {round(end_time - start_time, 2)} секунд")


if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    print(f"Количество ядер cpu: {num_cores}")
    # Количество ядер cpu: 4

    NUM_PROCESSES = int(input("Введите количество процессов: "))
    hash_values = [
        "1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad",
        "3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b",
        "74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f",
        "7a68f09bd992671bb3b19a5e70b7827e"
    ]
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    password_length = 5

    run_multiprocess_brute_force(NUM_PROCESSES, hash_values, ALPHABET, password_length)

    # Введите количество процессов: 1
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 43.66 секунд

    # Введите количество процессов: 2
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 27.55 секунд

    # Введите количество процессов: 3
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 25.63 секунд

    # Введите количество процессов: 4
    # Пароль: apple, SHA-256: 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b
    # Пароль: mmmmm, SHA-256: 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f
    # Пароль: testa, MD5: 7a68f09bd992671bb3b19a5e70b7827e
    # Пароль: zyzzx, SHA-256: 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad
    # Время выполнения: 27.14 секунд
