import time
import threading

_LOCK = threading.Lock()
_LAST = 0.0
_MIN_GAP_SEC = 0.10  # 10 req/sec max burst.

def throttle():
    global _LAST
    now = time.time()
    with _LOCK:
        gap = now - _LAST
        if gap < _MIN_GAP_SEC:
            time.sleep(_MIN_GAP_SEC - gap)
        _LAST = time.time()
