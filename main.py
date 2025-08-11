from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel, Field
from fastapi import Query, HTTPException
from jamo import h2j, j2hcj

app = FastAPI(title="api2")

class DecomposeIn(BaseModel):
    text: str = Field(..., description="분해할 문자열")
    compat: bool = Field(False, description="호환 자모로 변환할지 여부")

class DecomposeOut(BaseModel):
    original: str
    jamo: str
    jamo_list: list[str]

class DecomposeBatchIn(BaseModel):
    texts: list[str] = Field(..., description="분해할 문자열들의 리스트")
    compat: bool = Field(False, description="호환 자모로 변환할지 여부")

class DecomposeBatchOutItem(BaseModel):
    original: str
    jamo: str
    jamo_list: list[str]

class DecomposeBatchOut(BaseModel):
    results: list[DecomposeBatchOutItem]

def _decompose(text: str, compat: bool = False) -> tuple[str, list[str]]:
    """
    한글 음절을 자모로 분해(h2j). compat=True면 호환 자모(j2hcj)로 매핑.
    반환: (자모 문자열, 자모 리스트)
    """
    try:
        decomposed = h2j(text)
        if compat:
            decomposed = j2hcj(decomposed)
        # 문자열과 리스트를 함께 제공
        jamo_list = list(decomposed)
        return decomposed, jamo_list
    except Exception as e:
        # 예상치 못한 에러를 FastAPI 에러로 래핑
        raise HTTPException(status_code=400, detail=f"decompose failed: {e}")

@app.post("/jamo/decompose", response_model=DecomposeOut)
def jamo_decompose(payload: DecomposeIn):
    jamo_str, jamo_list = _decompose(payload.text, payload.compat)
    return DecomposeOut(original=payload.text, jamo=jamo_str, jamo_list=jamo_list)

@app.post("/jamo/decompose/batch", response_model=DecomposeBatchOut)
def jamo_decompose_batch(payload: DecomposeBatchIn):
    results: list[DecomposeBatchOutItem] = []
    for t in payload.texts:
        jamo_str, jamo_list = _decompose(t, payload.compat)
        results.append(DecomposeBatchOutItem(original=t, jamo=jamo_str, jamo_list=jamo_list))
    return DecomposeBatchOut(results=results)

@app.get("/jamo/decompose", response_model=DecomposeOut)
def jamo_decompose_query(
    text: str = Query(..., description="분해할 문자열"),
    compat: bool = Query(False, description="호환 자모로 변환할지 여부"),
):
    jamo_str, jamo_list = _decompose(text, compat)
    return DecomposeOut(original=text, jamo=jamo_str, jamo_list=jamo_list)

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

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>API2 메인</title>
        </head>
        <body>
            <h1>API2 사용 예시</h1>
            <ul>
                <li>
                    <strong>Ping 테스트</strong><br>
                    <code>GET /ping</code><br>
                    예: <a href="/ping" target="_blank">/ping</a>
                </li>
                <li>
                    <strong>헬스 체크</strong><br>
                    <code>GET /healthz</code><br>
                    예: <a href="/healthz" target="_blank">/healthz</a>
                </li>
                <li>
                    <strong>한글 자모 분해 (Query)</strong><br>
                    <code>GET /jamo/decompose?text=한글&compat=true</code><br>
                    예: <a href="/jamo/decompose?text=한글&compat=true" target="_blank">/jamo/decompose?text=한글&compat=true</a>
                </li>
                <li>
                    <strong>한글 자모 분해 (POST, 단일)</strong><br>
                    <code>POST /jamo/decompose</code><br>
                    Body(JSON): <pre>{ "text": "한글", "compat": true }</pre>
                </li>
                <li>
                    <strong>한글 자모 분해 (POST, 배치)</strong><br>
                    <code>POST /jamo/decompose/batch</code><br>
                    Body(JSON): <pre>{ "texts": ["한글", "테스트"], "compat": false }</pre>
                </li>
                <li>
                    <strong>소인수분해</strong><br>
                    <code>GET /factorize/360</code><br>
                    예: <a href="/factorize/360" target="_blank">/factorize/360</a>
                </li>
            </ul>
        </body>
    </html>
    """

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
