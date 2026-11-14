
from datetime import datetime

from pawpal_system import Owner, Pet, Task
from ai_advisor import build_safe_schedule, validate_schedule


def make_owner(task_specs):
    pet = Pet("Buddy", "dog")
    for description, hour, minute, duration in task_specs:
        pet.add_task(Task(
            description,
            datetime(2026, 11, 14, hour, minute),
            duration_minutes=duration
        ))
    return Owner("Test", [pet])


def test_overlapping_walks_are_rescheduled():
    owner = make_owner([
        ("Morning walk", 8, 0, 20),
        ("Second walk", 8, 0, 20),
    ])
    entries = build_safe_schedule(owner)

    assert validate_schedule(entries)[0]
    assert entries[0]["start"] == "2026-11-14T08:00:00"
    assert entries[1]["start"] == "2026-11-14T08:20:00"


def test_task_durations_are_preserved():
    owner = make_owner([
        ("Walk", 8, 0, 20),
        ("Feeding", 8, 10, 15),
    ])
    entries = build_safe_schedule(owner)

    assert validate_schedule(entries)[0]
    assert all(e["duration_minutes"] > 0 for e in entries)


def test_medication_time_is_protected():
    owner = make_owner([
        ("Walk", 8, 0, 20),
        ("Medication", 8, 10, 10),
    ])
    entries = build_safe_schedule(owner)

    medication = next(e for e in entries if e["task"] == "Medication")
    walk = next(e for e in entries if e["task"] == "Walk")

    assert medication["start"] == "2026-11-14T08:10:00"
    assert walk["start"] == "2026-11-14T08:20:00"
    assert validate_schedule(entries)[0]


def test_overlapping_medications_are_rejected():
    owner = make_owner([
        ("Medication", 8, 0, 20),
        ("Insulin injection", 8, 10, 10),
    ])
    entries = build_safe_schedule(owner)

    valid, message = validate_schedule(entries)
    assert not valid
    assert "Overlapping tasks" in message


def test_empty_schedule_is_rejected():
    assert validate_schedule([])[0] is False


def test_incorrect_duration_is_rejected():
    owner = make_owner([("Walk", 8, 0, 20)])
    entries = build_safe_schedule(owner)
    entries[0]["end"] = "2026-11-14T08:10:00"

    assert validate_schedule(entries)[0] is False
