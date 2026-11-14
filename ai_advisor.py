

"""PawPal AI scheduling advisor with deterministic safety checks."""

import json
from datetime import timedelta
from urllib import request, error

from pawpal_system import Scheduler

MODEL = "gemma3:1b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Tasks with medical or strict timing requirements must not be moved automatically.
PROTECTED_KEYWORDS = (
    "medication", "medicine", "insulin", "injection",
    "prescription", "vaccine", "emergency"
)


def is_protected(task):
    """Identify tasks requiring human review before rescheduling."""
    return any(
        word in task.description.lower()
        for word in PROTECTED_KEYWORDS
    )



def build_safe_schedule(owner):
    """Schedule flexible tasks around protected time intervals."""
    scheduler = Scheduler(owner)
    tasks = [
        (pet, task)
        for pet, task in scheduler.sort_by_time()
        if not task.completed
    ]

    for _, task in tasks:
        if task.duration_minutes <= 0:
            raise ValueError("Task duration must be positive.")

    protected = [
        (task.due_time,
         task.due_time + timedelta(minutes=task.duration_minutes))
        for _, task in tasks if is_protected(task)
    ]
    protected.sort()

    entries = []
    previous_end = None

    for pet, task in tasks:
        original = task.due_time

        if is_protected(task):
            start = original
            end = start + timedelta(minutes=task.duration_minutes)
            status = "REQUIRES HUMAN REVIEW"
            reason = "Protected task: original time preserved; confirm with owner."
        else:
            start = max(original, previous_end) if previous_end else original

            # Move flexible tasks past protected intervals.
            while True:
                end = start + timedelta(minutes=task.duration_minutes)
                overlap = next(
                    ((a, b) for a, b in protected
                     if start < b and a < end),
                    None
                )
                if overlap is None:
                    break
                start = overlap[1]

            end = start + timedelta(minutes=task.duration_minutes)
            status = "PROPOSED" if start != original else "UNCHANGED"
            reason = "Flexible task scheduled without protected-time overlap."
            previous_end = end

        entries.append({
            "pet": pet.name,
            "task": task.description,
            "status": status,
            "reason": reason,
            "original_start": original.isoformat(),
            "start": start.isoformat(),
            "end": end.isoformat(),
            "duration_minutes": task.duration_minutes
        })

    return entries



def validate_schedule(entries):
    """Validate durations, protected times, and all task overlaps."""
    if not entries:
        return False, "No pending tasks to schedule."
    from datetime import datetime

    intervals = []

    for entry in entries:
        start = datetime.fromisoformat(entry["start"])
        end = datetime.fromisoformat(entry["end"])
        original = datetime.fromisoformat(entry["original_start"])
        duration = entry["duration_minutes"]

        if duration <= 0 or end - start != timedelta(minutes=duration):
            return False, f"Invalid duration: {entry['task']}"

        if entry["status"] == "REQUIRES HUMAN REVIEW":
            if start != original:
                return False, f"Protected task was moved: {entry['task']}"

        intervals.append((start, end, entry["task"]))

    # Sort by actual scheduled time, not original task order.
    intervals.sort(key=lambda item: item[0])

    for previous, current in zip(intervals, intervals[1:]):
        if current[0] < previous[1]:
            return False, (
                f"Overlapping tasks: {previous[2]} and {current[2]}"
            )

    return True, "All task durations and protected times are valid; no overlaps."


def explain_with_gemma(entries):
    """Ask the local model to explain, not recalculate, the schedule."""
    valid, reason = validate_schedule(entries)

    if not valid:
        return f"AI explanation blocked: {reason}"

    prompt = (
        "You are PawPal's pet-care scheduling assistant. "
        "The following schedule was calculated and validated by Python. "
        "Explain briefly why tasks were ordered this way. "
        "Do not calculate, change, or invent any times. "
        "Do not give veterinary medical advice. "
        "Tasks marked REQUIRES HUMAN REVIEW must not be rescheduled "
        "without the owner's or veterinarian's approval. "
        "Use the supplied schedule exactly:\n"
        + json.dumps(entries, indent=2)
    )

    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0}
    }).encode("utf-8")

    try:
        req = request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with request.urlopen(req, timeout=90) as response:
            result = json.load(response)

        explanation = result.get("response", "").strip()

        # Gemma's explanation is advisory, not authoritative.
        # Reject unsupported claims about priority or veterinary care.
        unreliable_phrases = (
            "most important",
            "highest priority",
            "veterinary appointment",
            "physical examination",
            "physical exam",
        )

        if any(phrase in explanation.lower() for phrase in unreliable_phrases):
            return (
                "AI explanation withheld because it contained "
                "unsupported claims. Python has independently "
                "validated the proposed schedule. Tasks are "
                "organized by scheduled time, with their "
                "durations preserved."
            )

        return explanation or "No AI explanation was generated."

    except (error.URLError, TimeoutError, OSError, ValueError) as exc:
        return (
            "Gemma is unavailable. The validated Python schedule "
            f"is still available. Details: {exc}"
        )
