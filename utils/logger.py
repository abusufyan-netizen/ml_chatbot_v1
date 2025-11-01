import json, os, time
LOG = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'session_log.txt')
def log(msg):
    with open(LOG, 'a') as f:
        f.write(f"{time.asctime()} - {msg}\n")
def save_training_history(d):
    p = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'training_history.json')
    json.dump(d, open(p, 'w'), indent=2)
