from collections import defaultdict


def count_alerts(f):
    alerts = defaultdict(int)
    for line in f:
        alerts[line.strip()] += 1
    return dict(alerts)
