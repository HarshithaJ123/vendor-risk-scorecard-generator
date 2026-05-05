import requests
import json
from demo_data import demo_records

URL = "http://127.0.0.1:5000/ai/generate-report"

results = []

for record in demo_records:
    try:
        response = requests.post(URL, json=record)
        
        if response.status_code == 200:
            data = response.json()
            results.append(data)
            print(f"✅ {record['vendor']} processed")
        else:
            print(f"❌ Error for {record['vendor']}")

    except Exception as e:
        print(f"⚠️ Failed: {record['vendor']} → {e}")

# Save output
with open("demo_output.json", "w") as f:
    json.dump(results, f, indent=4)

print("\n🎉 All outputs saved to demo_output.json")