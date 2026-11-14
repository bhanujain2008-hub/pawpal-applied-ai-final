
# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design included four Python classes:

- **Owner:** Stores owner information, manages multiple pets, and retrieves tasks across all pets.
- **Pet:** Stores pet information and manages its assigned care tasks.
- **Task:** Represents a care activity, including its description, due date/time, frequency, priority, and completion status.
- **Scheduler:** Organizes tasks across multiple pets using sorting, filtering, recurrence, and conflict detection.

**Relationships:** One Owner can have multiple Pets, and each Pet can have multiple Tasks. The Scheduler accesses the Owner's combined task list.

**Core user actions:** Add a pet, schedule a care task, and view an organized daily schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I refined my initial design while preserving its four-class structure.

- Implemented `sort_by_priority()` to organize tasks by High, Medium, and Low priority, using due time to break ties.
- Used Python dataclasses for `Owner`, `Pet`, and `Task` to simplify initialization.
- Added `duration_minutes` to `Task`, defaulting to 20 minutes.
- Improved `Scheduler.detect_conflicts()` to detect overlapping time intervals rather than only identical start times.
- Added `storage.py` to save and restore owner, pet, and task information using JSON.
- Updated the final UML diagram to reflect the implemented duration attribute.

These changes made the scheduler more practical while preserving the original object-oriented design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers task due dates/times, durations, priority levels, pet identity, completion status, and recurrence frequency.

- **Time and duration:** Determine when tasks begin and end and whether they overlap.
- **Priority:** Helps identify important activities, such as medication.
- **Pet identity:** Allows owners to view tasks for individual pets.
- **Completion status:** Supports filtering and recurring-task processing.
- **Recurrence:** Supports daily and weekly care activities.

Time and duration are essential for identifying scheduling conflicts, while priority helps owners decide which tasks deserve attention first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler detects overlapping tasks but does not automatically reschedule them.

For example:

- Feeding starts at 10:00 AM and lasts 30 minutes.
- Medication starts at 10:15 AM and lasts 20 minutes.

The scheduler correctly identifies the overlap but leaves the scheduling decision to the pet owner.

This approach is reasonable because pet owners may have different preferences, flexibility, or constraints that the application cannot fully determine.

The scheduler also treats tasks that meet exactly at an endpoint as non-conflicting. A task ending at 10:30 AM does not conflict with another starting at 10:30 AM.

This provides clear, predictable behavior without introducing unnecessary scheduling complexity.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used ChatGPT and GitHub Copilot throughout the project.

**ChatGPT helped me:**

- Plan the UML design and class responsibilities.
- Implement the four Python classes.
- Develop scheduling algorithms.
- Create automated tests.
- Integrate the backend with Streamlit.
- Implement JSON persistence.
- Understand errors and verify results.
- Prepare project documentation.

**GitHub Copilot Agent helped me:**

- Add task durations.
- Improve conflict detection to identify overlapping intervals.
- Update the Streamlit interface and JSON storage.
- Add automated tests.
- Update the final UML diagram and README.
- Run verification commands.

I also used GitHub Copilot Ask mode to compare a broad prompt with a more specific prompt about improving conflict detection.

The most helpful prompts specified the relevant files, expected behavior, constraints, testing requirements, and restrictions on modifying existing code.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I chose to preserve CodePath's original `app.py` structure instead of replacing the starter interface with an unrelated implementation.

I also required GitHub Copilot Agent to inspect the existing project, preserve local JSON persistence changes, and avoid committing or pushing files automatically.

Rather than relying only on AI-generated explanations, I verified the implementation through:

- Running the command-line demonstration.
- Executing the automated pytest suite.
- Testing the Streamlit interface with multiple pets and tasks.
- Creating overlapping tasks and checking the conflict warnings.
- Inspecting saved JSON data to confirm task durations.
- Restarting Streamlit to verify saved pet information was restored.
- Reviewing the agent's reported file changes and test results.

The final automated test run passed all 11 tests.

The detailed agent workflow and prompt comparison are documented in `ai_interactions.md`.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The original implementation had seven passing automated tests. After the duration-aware scheduling improvements, the test suite increased to 11 tests.

The tests cover:

1. Task completion.
2. Adding tasks to pets.
3. Chronological sorting across multiple pets.
4. Filtering tasks.
5. Detecting overlapping scheduling intervals.
6. Confirming that tasks meeting exactly at an endpoint do not conflict.
7. Preserving task durations during recurrence.
8. Saving and loading task durations.
9. Loading older JSON records without duration fields.
10. Creating recurring tasks.
11. Sorting tasks by priority.

**Final automated test result:**

```text
collected 11 items

tests\test_pawpal.py ...........                           [100%]

====================== 11 passed in 0.18s =======================
```

**Manual browser verification:**

- Added multiple pets and care tasks.
- Generated schedules using the Streamlit interface.
- Confirmed conflict warnings appeared.
- Tested Feeding at 10:00 AM for 30 minutes and Medication at 10:15 AM for 20 minutes.
- Confirmed the application detected their overlapping intervals.
- Inspected `pawpal_data.json` and verified both durations were saved correctly.
- Previously restarted Streamlit and confirmed saved pet information was restored.

These tests helped verify that the Python classes, scheduling algorithms, user interface, and JSON persistence worked together.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

**Confidence: 4/5.**

All 11 automated tests passed, and the important scheduling and persistence features were verified manually.

Additional testing could cover:

- Pets without tasks.
- Weekly recurrence.
- Invalid or negative task durations.
- Duplicate task descriptions.
- Nested and multiple overlapping intervals.
- Mixed timezone-aware and timezone-naive dates.
- Completed tasks that still overlap with pending tasks.
- More extensive persistence testing after restarting the application.

These tests would improve reliability and help identify unusual scheduling conditions.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with integrating the object-oriented Python backend into a working Streamlit application.

The project evolved from a UML design into a functioning scheduling system that supports multiple pets, task priorities, durations, recurrence, conflict detection, and JSON persistence.

I am also satisfied that the GitHub Copilot Agent improvements were verified through automated tests and a real browser demonstration.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would focus on:

- Allowing users to edit existing tasks.
- Automatically suggesting alternative times for conflicting tasks.
- Validating invalid durations and inconsistent datetime values.
- Providing clearer explanations of overlapping time windows.
- Improving how completed tasks are handled in conflict detection.
- Adding more automated edge-case tests.
- Improving the interface for larger schedules involving many pets.

JSON persistence and duration-aware conflict detection were originally possible future improvements, but both were implemented during this project.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that AI can accelerate software design, implementation, and testing, but the developer must still define requirements, evaluate suggestions, and verify results.

The project reinforced several important lessons:

- Design the system before writing code.
- Separate the scheduling backend from the user interface.
- Preserve existing functionality when adding features.
- Use specific prompts with clear constraints.
- Test important behavior rather than assuming generated code is correct.
- Review and verify autonomous AI agent changes before committing them.

The most valuable lesson was that **AI-assisted development works best when clear requirements, careful human judgment, and systematic testing are combined**.


---

## 6. AI110 Final Project 4 — Applied AI Extension

### a. Project Evolution

I extended my original Module 2 PawPal+ application by integrating an AI Scheduling Advisor powered by Google's Gemma 3 1B model through Ollama.

I preserved the original four-class architecture, Streamlit interface, JSON persistence, scheduling functions, and automated tests.

The new advisor proposes schedules for pending tasks, validates their timing, protects medication-related tasks, and uses Gemma to explain validated schedules.

Unlike the original scheduler, which detects conflicts without changing task times, the new advisor proposes alternative times for flexible tasks. These proposals do not automatically overwrite saved tasks.

### b. Model Selection and Evaluation

I selected Gemma 3 1B because it can run locally through Ollama without requiring a cloud API.

Before integrating the model, I tested its ability to reason about scheduling constraints.

I discovered several important limitations:

- Gemma assigned only 10 minutes to tasks that required 20 minutes.
- Even with explicit instructions, it shortened a 20-minute task to two minutes.
- It invented activities and veterinary examinations that were absent from the input.
- It claimed that an evening walk was the most important task without sufficient justification.

These failures demonstrated that an LLM should not be trusted to calculate scheduling intervals independently.

### c. Engineering Decisions and AI Collaboration

**Accepted AI suggestion:** Separate deterministic scheduling from natural-language explanations. Python calculates and validates the schedule, while Gemma explains it.

**Revised AI suggestion:** The initial scheduling implementation did not adequately protect medication times. I revised the algorithm to reserve protected intervals before moving flexible tasks.

I also added validation for task durations, overlapping intervals, and empty schedules.

A basic phrase-based safeguard was introduced after Gemma generated unsupported claims. However, this safeguard is not a comprehensive hallucination detector.

### d. Testing and Verification

The original Module 2 project contained 11 passing tests.

Final Project 4 added six tests covering:

- Rescheduling overlapping flexible tasks.
- Preserving task durations.
- Protecting medication times.
- Rejecting conflicting protected tasks.
- Rejecting empty schedules.
- Detecting incorrect task durations.

**Latest verified result: 17 tests passed.**

I also verified the integrated Streamlit application and observed Gemma's explanations in the browser.

These tests establish confidence in the tested Python scheduling safeguards, but they do not prove that every AI explanation will be accurate.

### e. Remaining Limitations

The system does not understand veterinary medical requirements, owner availability, travel time, or all practical constraints.

Protected tasks are identified using keywords, which may miss unusual descriptions.

Gemma may still generate unsupported explanations that bypass the phrase filter.

Future improvements should include structured model outputs, stronger explanation validation, additional automated model tests, and owner-configurable scheduling constraints.

### f. Final Takeaway

The most important lesson from Final Project 4 was that **integrating AI successfully requires more than obtaining a plausible model response**.

I learned to test the model against explicit constraints, identify its failures, revise the architecture accordingly, and use deterministic validation to protect critical application behavior.

The resulting system combines the strengths of conventional software engineering with the flexibility of AI-generated explanations while acknowledging the limitations of both.