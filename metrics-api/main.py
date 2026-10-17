import time
import uuid

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "22f3002678@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-mr8krf.example.com"

app = FastAPI()


# --- Middleware 1: add X-Request-ID and X-Process-Time to EVERY response ---
@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


# --- Middleware 2: CORS, only for our one allowed origin ---
# Added AFTER the function above, so it sits on the outside and
# also handles preflights before they reach anything else.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],   # exact match, no "*"
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/stats")
def stats(values: str = Query(...)):
    try:
        nums = [int(v) for v in values.split(",") if v.strip() != ""]
    except ValueError:
        raise HTTPException(status_code=400, detail="values must be integers")

    if not nums:
        raise HTTPException(status_code=400, detail="no values given")

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }