"""Percent Change Times List.
Stores time in seconds.
"""
supported_times = [
    ("24 hours", 86400),
    ("1 week", 604800)
]

times = []
for i in range(len(supported_times)):
    times.append((i, supported_times[i][0]))
