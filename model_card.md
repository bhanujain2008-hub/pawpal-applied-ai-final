

# Model Card — PawPal+ AI Scheduling Advisor

## 1. Model Information

- **Model:** Google Gemma 3 1B (`gemma3:1b`)
- **Runtime:** Ollama, running locally
- **Application:** PawPal+ AI110 Final Project 4
- **Role:** Explain schedules calculated and validated by Python
- **Access:** Local Ollama API at `http://localhost:11434/api/generate`

## 2. Intended Use

The model provides brief, understandable explanations of proposed pet-care schedules.

Python, not Gemma, calculates task start times, end times, and durations.

The application is intended for general pet-care planning, not veterinary diagnosis, treatment, or medication decisions.

## 3. System Architecture

1. The owner enters tasks through Streamlit.
2. Python schedules pending tasks.
3. Protected tasks retain their original times.
4. Python validates durations and overlapping intervals.
5. Invalid schedules block AI explanations.
6. Valid schedules are submitted to Gemma.
7. A basic output safeguard checks for certain unsupported claims.
8. The interface displays the validated schedule and advisory explanation.

Architecture source: `diagrams/architecture.mmd`.

## 4. Evaluation Method

The system was evaluated using:

- Direct prompts to Gemma about scheduling.
- Manual Streamlit demonstrations.
- Six new automated scheduling reliability tests.
- Eleven original PawPal+ functionality tests.

**Verified automated result: 17/17 tests passed.**

These tests primarily verify Python scheduling and validation, not the factual accuracy of every model-generated explanation.

## 5. Observed Model Failures

### Failure A — Incorrect Duration Arithmetic

For two 20-minute tasks, Gemma proposed:

    7:40–7:50 AM: Walk (20 minutes)
    7:50–8:00 AM: Feeding (20 minutes)

Both intervals lasted only 10 minutes.

### Failure B — Incorrect Sequential Scheduling

When instructed not to shorten two 20-minute tasks, Gemma proposed:

    8:00–8:20 AM: Task 1
    8:20–8:22 AM: Task 2

Task 2 lasted only two minutes.

### Failure C — Hallucinated Activities

Gemma described additional activities and increasing task durations when the input contained only one walk.

For an empty schedule, it invented veterinary appointments and examinations.

### Failure D — Unsupported Priority Ranking

Gemma described an evening walk as the "most important" task even though the scheduler had not established that priority.

## 6. Safeguards

- Deterministic Python calculations replace LLM scheduling arithmetic.
- Task durations are checked against actual time intervals.
- All proposed intervals are checked for overlaps.
- Medication and other keyword-identified protected tasks retain their original times.
- Conflicting protected tasks require human review.
- Empty schedules are rejected.
- Invalid schedules block AI explanations.
- A phrase-based filter rejects several previously observed unsupported claims.
- The validated Python schedule remains authoritative.
- AI-generated explanations do not modify saved tasks.

## 7. Limitations and Risks

### Model Limitations

- Gemma may hallucinate tasks, priorities, explanations, or times.
- Temperature zero does not guarantee factual accuracy.
- The phrase filter detects only selected expressions.
- Model responses may be misleading even when the Python schedule is valid.

### Scheduling Limitations

- Protected tasks are recognized using description keywords.
- The system does not understand veterinary medical requirements.
- Owner availability, travel time, and pet-specific needs are not fully modeled.
- A nonoverlapping schedule is not necessarily practical or medically appropriate.
- Protected-task conflicts are detected but not automatically resolved.

### Potential Bias

- Explanations may reflect assumptions about common pet-care routines.
- Unusual pets, specialized care requirements, and less common owner circumstances may be poorly represented.
- English-language prompts and task descriptions are the primary tested use case.

## 8. Misuse and Out-of-Scope Uses

Do not use PawPal+ to:

- Determine medication doses.
- Automatically change medication timing.
- Diagnose or treat animal illnesses.
- Replace veterinary advice.
- Make emergency pet-care decisions.
- Assume every AI explanation is correct.

## 9. Privacy

Gemma runs locally through Ollama.

PawPal+ stores owner and pet information in a local JSON file. The project excludes `pawpal_data.json` from Git tracking.

Local processing reduces dependence on external model services but does not eliminate device, software, or data-security risks.

## 10. Improvements and Future Evaluation

Potential improvements include:

- Structured AI responses with schema validation.
- Automatic checks that explanations reference only supplied tasks and times.
- Tests using mocked Ollama responses.
- Broader testing of medication-related descriptions.
- Evaluation across different pet species and care routines.
- Owner-configurable scheduling constraints.
- Additional human review before accepting proposed changes.

## 11. Overall Assessment

**Strength:** Python-based scheduling and validation performed correctly in the tested scenarios.

**Weakness:** Gemma 3 1B produced several incorrect or unsupported explanations.

**Conclusion:** The model is useful as a supplementary explanation tool, but it is not sufficiently reliable to calculate schedules or make medical decisions independently.

The application therefore separates deterministic scheduling from AI-generated explanations.
