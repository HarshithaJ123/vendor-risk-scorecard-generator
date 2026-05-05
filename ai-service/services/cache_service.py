# 🔴 REDIS DISABLED (Day 11)

def generate_key(vendor, risk_score):
    return f"{vendor}:{risk_score}"

def get_cache(key):
    return None   # always skip cache

def set_cache(key, value):
    pass          # do nothing

