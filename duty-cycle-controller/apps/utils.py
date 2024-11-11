from datetime import datetime, timedelta


def calculate_duty_cycle_from_history(history, duration, now=None):
    """
    Calculates the duty cycle for a given history data set.

    Parameters:
    - history: List of state entries, each entry containing 'state' and 'last_changed'.
    - duration: The total duration to analyze as a timedelta object.
    - now: Optional fixed "now" time for consistent testing.

    Returns:
    - duty cycle as a float between 0 and 1.
    """
    if not history:
        return 0.0

    now = now or datetime.now()
    on_time = 0.0
    total_time = duration.total_seconds()

    last_state = None
    last_timestamp = None

    for entry in history:
        state = entry["state"]
        timestamp = datetime.fromisoformat(entry["last_changed"])

        if last_state == "on" and last_timestamp:
            on_time += (timestamp - last_timestamp).total_seconds()

        last_state = state
        last_timestamp = timestamp
        print(f"on_time: {on_time}, total_time: {total_time} {timestamp}")

    # If the last recorded state was "on", count time until now
    if last_state == "on" and last_timestamp:
        on_time += (datetime.now() - last_timestamp).total_seconds()

    # Calculate duty cycle
    duty_cycle = on_time / total_time if total_time > 0 else 0
    print(f"on_time: {on_time}, total_time: {total_time}: {duty_cycle}")

    return duty_cycle
