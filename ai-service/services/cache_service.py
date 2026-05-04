import redis
import json
import hashlib

# Connect to Redis
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

# TTL = 15 minutes (900 seconds)
TTL = 900

# 🔑 Generate SHA256 key
def generate_key(vendor, risk_score):
    raw = f"{vendor}:{risk_score}"
    return hashlib.sha256(raw.encode()).hexdigest()

# 📥 Get from cache
def get_cache(key):
    data = redis_client.get(key)
    if data:
        print("⚡ CACHE HIT")
        return json.loads(data)
    return None

# 📤 Set cache WITH TTL
def set_cache(key, value):
    redis_client.setex(
        key,
        TTL,  # ⏱️ THIS IS IMPORTANT
        json.dumps(value)
    )
    print("💾 SAVED TO CACHE")