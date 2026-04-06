import requests
import time
import statistics

VM_IP = "http://34.58.136.223:5000"

FAST_URL = f"{VM_IP}/insert-fast"
SAFE_URL = f"{VM_IP}/insert-safe"

def benchmark(url, label, n=50):
    times = []

    for i in range(n):
        payload = {
            "VIN (1-10)": f"TESTVIN{i}",
            "City": "Seattle",
            "Make": "TESLA",
            "Model": "MODEL 3",
            "Model Year": 2022
        }

        start = time.time()
        response = requests.post(url, json=payload)
        end = time.time()

        latency_ms = (end - start) * 1000
        times.append(latency_ms)

        print(f"{label} Request {i+1}: {latency_ms:.2f} ms | Status: {response.status_code}")

    avg = statistics.mean(times)
    print(f"\n{label} Average Latency: {avg:.2f} ms")
    return avg

fast_avg = benchmark(FAST_URL, "FAST WRITE")
safe_avg = benchmark(SAFE_URL, "SAFE WRITE")

print("\n==============================")
print(f"FAST WRITE AVG: {fast_avg:.2f} ms")
print(f"SAFE WRITE AVG: {safe_avg:.2f} ms")
print("==============================")