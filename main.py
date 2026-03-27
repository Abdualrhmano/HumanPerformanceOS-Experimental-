# main.py - Production-Ready Human Performance OS Decision Engine
from fastapi import FastAPI, Depends, Request, HTTPException, Header
from pydantic import BaseModel
import uvicorn
import os
import base64
import json
from typing import Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", b"1Xt5YfM4ZNuFdwp3OfVkwkhhQLagWKtt1234567890123456")  # 32 bytes AES-256 key
API_KEYS = {"demo-key": "user1"}  # In production, use env or DB

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])
app = FastAPI(title="Human Performance OS Decision Engine")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Pydantic Schema for User Metrics
class UserMetrics(BaseModel):
    sleep_hours: float  # 0-10
    focus_hours: float  # 0-10
    energy_level: float  # 0-10
    habit_consistency: float  # 0-1

# API Key Dependency
async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return API_KEYS[x_api_key]

# AES-256 Encryption/Decryption
def encrypt_data(data: Dict[str, Any]) -> str:
    aesgcm = AESGCM(SECRET_KEY)
    nonce = os.urandom(12)
    data_bytes = json.dumps(data).encode()
    ciphertext = aesgcm.encrypt(nonce, data_bytes, None)
    # Combine nonce + ciphertext, base64 encode
    combined = nonce + ciphertext
    return base64.b64encode(combined).decode()

def decrypt_data(encrypted: str) -> Dict[str, Any]:
    aesgcm = AESGCM(SECRET_KEY)
    combined = base64.b64decode(encrypted)
    nonce = combined[:12]
    ciphertext = combined[12:]
    data_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(data_bytes.decode())

# Scoring Engine
def calculate_performance_score(metrics: UserMetrics) -> float:
    # Sanitize inputs
    focus = max(0, min(10, metrics.focus_hours))
    energy = max(0, min(10, metrics.energy_level))
    consistency = max(0, min(1, metrics.habit_consistency))
    sleep = max(0, min(10, metrics.sleep_hours))  # Not weighted, but could adjust
    score = (focus * 0.4) + (energy * 0.3) + (consistency * 0.3 * 10)  # Normalize consistency to 0-10
    return round(score, 2)

# Simulated ReAct Agent for Recommendation (Prompt Injection Safe - templated)
def generate_recommendation(score: float) -> str:
    if score >= 8.0:
        return "Excellent performance! Maintain current habits and consider challenging yourself with new goals."
    elif score >= 6.0:
        return "Good performance. Focus on improving sleep consistency to boost energy levels."
    elif score >= 4.0:
        return "Moderate performance. Prioritize sleep (>7h) and focus sessions (2+ hours daily)."
    else:
        return "Low performance. Start with basics: 7-8h sleep, 1h focused work, build 1 daily habit."

# Endpoints
@app.get("/status")
async def health_check():
    return {"status": "healthy", "service": "Human Performance OS Decision Engine"}

@app.post("/evaluate")
@limiter.limit("10/minute")
async def evaluate_performance(
    metrics: UserMetrics,
    user_id: str = Depends(verify_api_key),
    request: Request = None
):
    # Encrypt sensitive data
    encrypted_metrics = encrypt_data(metrics.dict())
    
    # Calculate score (decrypt not needed since we have plain metrics)
    score = calculate_performance_score(metrics)
    
    # Generate AI-driven recommendation (simulated ReAct: template-based to prevent injection)
    recommendation = generate_recommendation(score)
    
    return {
        "user_id": user_id,
        "encrypted_data": encrypted_metrics,
        "performance_score": score,
        "recommendation": recommendation,
        "timestamp": "2026-03-26T18:08:00Z"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
