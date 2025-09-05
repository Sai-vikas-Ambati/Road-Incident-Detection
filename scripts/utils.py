def log_event(event_type, message):
    print(f"[{event_type.upper()}] {message}")

def save_results(filename, results):
    with open(filename, "w") as f:
        for r in results:
            f.write(str(r) + "\n")
