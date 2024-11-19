from datetime import datetime, timedelta, timezone


def split(entry):
    state = entry["state"]
    timestamp = datetime.fromisoformat(entry["last_changed"])
    return state, timestamp


def parse_iso_to_datetime(iso_string):
    return datetime.fromisoformat(iso_string)


def get_state(history, timestamp):
    """
    Returns the state at a given timestamp by searching through the history list.
    Assumes the history is ordered from oldest to newest.

    :param history: List of dictionaries with 'state' and 'last_changed' as ISO strings.
    :param timestamp: The timestamp to check the state for.
    :return: The state at the given timestamp or None if not found.
    """
    for i in range(len(history) - 1):
        entry = history[i + 1]["last_changed"]
        next_state = parse_iso_to_datetime(entry)
        if timestamp <= next_state:
            return history[i]["state"]
    return history[-1]["state"]


def calculate_duty_cycle_from_history(history, duration, end_time=datetime.now()):
    """
    Calculates the duty cycle from a history list containing state change timestamps.

    :param history: List of dictionaries with 'state' and 'last_changed' as ISO strings.
    :return: The duty cycle as a percentage (percentage of time in the 'on' state).
    """
    if not history:
        return 0

    if isinstance(end_time, str):
        end_time = parse_iso_to_datetime(end_time)

    assert isinstance(end_time, datetime)
    if not end_time.tzinfo:
        end_time = end_time.replace(tzinfo=timezone.utc)

    modified_history = []
    last_valid_entry = None
    start_time = end_time - duration

    for entry in history:
        state, time = split(entry)
        if time <= start_time:
            last_valid_entry = (
                entry  # Keep track of the last valid entry before start_time
            )
        elif start_time < time <= end_time:
            modified_history.append(entry)

    if last_valid_entry:
        # Modify the last valid entry to have last_changed as start_time
        last_valid_entry = last_valid_entry.copy()
        last_valid_entry["last_changed"] = start_time.isoformat()
        modified_history.insert(0, last_valid_entry)

    print(f"Why duration={duration}  and end_time={end_time}, start_time={start_time}")
    for e in history:
        print(str(e))

    history = modified_history
    cur_state, cur_time = split(history[0])
    assert cur_time.tzinfo

    total_time_on = timedelta(0)
    total_time = timedelta(0)

    def add_interval(state, delta):
        nonlocal total_time, total_time_on
        total_time += delta
        if state == "on":
            total_time_on += delta
        print(f"add_interval {state} {delta}")

    for e in history[1:]:
        print(e)
        next_state, next_time = split(e)
        delta = next_time - cur_time
        add_interval(cur_state, delta)
        cur_state, cur_time = next_state, next_time

    delta = end_time - cur_time
    add_interval(cur_state, delta)

    duty_cycle = total_time_on / total_time
    return duty_cycle
