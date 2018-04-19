"""Percent Change Times List.

Stores time in seconds.
"""

supported_times = [
    ("1 hour", 3600),
    ("24 hours", 86400),
    ("1 week", 604800)
]

supported_durations = {
    "coinbase": ["86400"],
    "gemini": ["86400"],
    "bitfinex": [],
    "gdax": ["3600", "86400", "604800"],
    "nasdaq": []
}

times = []
for i in range(len(supported_times)):
    times.append((supported_times[i][1], supported_times[i][0]))
