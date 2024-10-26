import httpx

params = {
    "username": "USER", "password": "PASS"
}

# http://127.0.0.35:8000/vulnerabilities/brute/registration?username=USER&password=PASS
response = httpx.get(url="http://127.0.0.35:8000/vulnerabilities/brute/registration", params=params)

print(response.json())

# http://127.0.0.35:8000/vulnerabilities/brute/login?username=USER&password=PASS
response = httpx.get(url="http://127.0.0.35:8000/vulnerabilities/brute/login", params=params)

print(response.json())


params = {
    "username": "USER", "password": "INVALID_PASS"
}

print(f"\nBrute force process:")
for i in range(1, 10 + 1):
    # http://127.0.0.35:8000/vulnerabilities/brute/login?username=USER&password=INVALID_PASS
    response = httpx.get(url="http://127.0.0.35:8000/vulnerabilities/brute/login", params=params)

    print(f"{i}: {response.json()}")
