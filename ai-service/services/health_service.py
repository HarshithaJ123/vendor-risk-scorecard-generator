import time

# Track uptime
START_TIME = time.time()

# Track response times
response_times = []

def record_response_time(duration):
    response_times.append(duration)

def get_health_status():
    uptime = time.time() - START_TIME
    avg_time = sum(response_times)/len(response_times) if response_times else 0

    return {
        "status": "OK",
        "model": "llama-3.1-8b-instant",
        "avg_response_time_ms": round(avg_time * 1000, 2),
        "uptime_seconds": round(uptime, 2)
    }