from collections import deque
import statistics

# How many past points to remember
WINDOW_SIZE = 30

# How many standard deviations away counts as anomaly
Z_THRESHOLD = 2.5

# Minimum history length before we start detecting anomalies
MIN_POINTS = 5

def make_history(window_size: int = WINDOW_SIZE):
	"""
	Create a new rolling history buffer (a deque) that automatically drops old values when it gets full.
	"""
	return deque(maxlen=window_size)

def detect_anomaly(value, history, k: float = Z_THRESHOLD, min_points: int = MIN_POINTS):
	"""
	Statistical anomaly detection using rolling mean/std and z-score.

	-value: current numeric reading (e.g., CPU%, growth in MB)
	-history: deque containing previous readings

	Returns:
		(is_anomaly: bool, z-score: float)
	"""
	
	# First, add the new value to history
	history.append(value)

	# If we don't have enough points, we can't detect anomalies yet
	if len(history) < min_points:
		return False, 0.0

	mu = statistics.mean(history)
	sigma = statistics.pstdev(history)

	# If sigma is 0, all values are almost the same -> cannot compute useful z
	if sigma == 0:
		return False, 0.0

	# Calculate z-score
	z = (value - mu) / sigma
	return abs(z) > k, z