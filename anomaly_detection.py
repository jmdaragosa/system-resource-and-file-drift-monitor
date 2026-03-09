from collections import deque
import statistics

# How many past points to remember
WINDOW_SIZE = 30

# How many standard deviations away counts as anomaly
Z_THRESHOLD = 2.5

# Minimum history length before we start detecting anomalies
MIN_POINTS = 5

def make_history(window_size: int = WINDOW_SIZE):
	return deque(maxlen=window_size)
