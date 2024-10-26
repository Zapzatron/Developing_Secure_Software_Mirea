from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import uvicorn
import time


app = FastAPI()

# Для демонстрации
users_db = {
    # "user1": {"username": "user1", "hashed_password": "$2b$12$ftjDfaPXa.KEw8IoMRaXCe5TE0XDF53TVGWfHJBLCljw8EdFUYn8e"},
}

# Для хранения временных меток для 429
request_times = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_rate_limit(ip: str, limit: int = 5, period: int = 60 * 1):
    current_time = time.time()
    if ip not in request_times:
        request_times[ip] = []
    request_times[ip] = [t for t in request_times[ip] if current_time - t < period]
    if len(request_times[ip]) >= limit:
        return False
    request_times[ip].append(current_time)
    return True


@app.get("/vulnerabilities/brute/login")
async def login(request: Request, username: str, password: str):
    ip = request.client.host

    if not check_rate_limit(ip):
        error_code = 429
        error_json = {"error": {"message": "Too many requests.", "code": error_code}}
        return JSONResponse(content=error_json, status_code=error_code)

    user = users_db.get(username)

    # print(user)

    if not user or not pwd_context.verify(password, user["hashed_password"]):
        error_code = 403
        error_json = {"error": {"message": "Username and/or password incorrect.", "code": error_code}}
        return JSONResponse(content=error_json, status_code=error_code)

    # Либо открытие страницы и добавление jwt в куки
    jwt_token = "generated.jwt.token"

    return {"access_token": jwt_token, "token_type": "bearer"}


@app.get("/vulnerabilities/brute/registration")
async def registration(request: Request, username: str, password: str):
    user = users_db.get(username)

    if user:
        error_code = 403
        error_json = {"error": {"message": "Username already exists", "code": error_code}}
        return JSONResponse(content=error_json, status_code=error_code)

    hashed_password = pwd_context.hash(password)

    users_db[username] = {"username": username, "hashed_password": hashed_password}

    # Либо открытие страницы и добавление jwt в куки
    jwt_token = "generated.jwt.token"

    return {"access_token": jwt_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.35", port=8000)
