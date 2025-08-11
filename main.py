from fastapi import FastAPI
from typing import List

app = FastAPI(title="api2")

def get_prime_factors(n: int) -> List[int]:
    factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
       factors.append(n)
    return factors

@app.get("/")
def root():
    return {"message": "hello api2"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/factorize/{number}")
def factorize(number: int):
    """
    Performs prime factorization on the given number.
    """
    return {"number": number, "factors": get_prime_factors(number)}
