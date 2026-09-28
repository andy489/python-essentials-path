import os

from alerts import count_alerts


def store_alert(clash, folder=None):
    # BUG: Should be open("alert_log.txt", "a")
    storage_folder = folder or os.getcwd()
    with open(alerts_logfile(storage_folder), "a") as f:
        f.write(f"{clash}\n")


def fetch_alerts(folder=None):
    storage_folder = folder or os.getcwd()
    logfile = alerts_logfile(storage_folder)
    if not os.path.exists(logfile):
        return {}
    with open(logfile, "r") as f:
        return count_alerts(f)


def alerts_logfile(storage_folder):
    return os.path.join(storage_folder, "alert_log.txt")
