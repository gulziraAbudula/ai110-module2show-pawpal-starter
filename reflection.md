# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
There are several main behaviors pet owners should be able to perform:
1) enter basic owner and pet information.
2) add and edit tasks (duration + priority at minimum)
3) Generate a daily schedule/plan based on constraints and priorities
4) Display the plan clearly (and ideally explain the reasoning)
5) Include tests for the most important scheduling behaviors

- What classes did you include, and what responsibilities did you assign to each?
owner: 
    name: str
    email: str
    available_hours: int — Hours per day available for pet care
    ========
    __init__(name, email, available_hours)
    get_name() -> str
    set_name(name: str)
    get_email() -> str
    set_email(email: str)
    get_available_hours() -> int
    set_available_hours(hours: int)
pet: 
    name: str
    age: int — Years old
    breed: str — Breed type
    owner: Owner — Reference to the pet's owner
    =======
    __init__(name, age, breed, owner)
    get_name() -> str
    set_name(name: str)
    get_age() -> int
    set_age(age: int)
    get_breed() -> str
    set_breed(breed: str)
task:
    title: str — Task name (e.g., "Morning Walk")
    task_type: str — Category (walk, feeding, medication, play, grooming)
    frequency: str — How often (daily, twice_daily, weekly)
    duration: int — Minutes needed
    priority: int — 1 (critical) to 5 (optional)
    is_completed: bool — Whether done today
    pet: Pet — Which pet this task is for
    =======
    __init__(title, task_type, frequency, duration, priority, pet)
    get_title() -> str
    set_title(title: str)
    get_task_type() -> str
    set_task_type(task_type: str)
    get_duration() -> int
    set_duration(duration: int)
    get_priority() -> int
    set_priority(priority: int)
    get_frequency() -> str
    set_frequency(frequency: str)
    mark_completed() — Set is_completed = True
    get_completion_status() -> bool
daily schedule:
    tasks: list[Task] — All tasks to schedule
    scheduled_tasks: dict — Format: {task: start_hour} (e.g., {walk_task: 9} means 9am)
    =======
    __init__(tasks)
    schedule(owner: Owner, pets: List[Pet]) -> dict — Arrange tasks for given pets, return {task: start_hour}. Prioritizes by frequency + priority
    validate() -> bool — Check: no overlaps, total duration fits available hours, critical tasks included
    get_validation_errors() -> list[str] — Return list of problems (if any)
    explain() -> str — Simple explanation: "Task X at 9am because it's priority 1" format
    get_scheduled_tasks() -> dict — Retrieve the generated schedule
    get_validation_errors() -> list[str] — Return list of problems (if any)
    explain() -> str — Simple explanation: "Task X at 9am because it's priority 1" format


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

**Changes made after initial review:**

1. **Added `owner: Owner` attribute to Pet class**
   - Reason: Each pet needs to know which owner is responsible for it. This establishes the relationship and allows the app to organize pets by owner.

2. **Added `pet: Pet` attribute to Task class**
   - Reason: Critical for the scheduler to know which pet each task is for. Without this, we can't distinguish between "walk for the dog" vs "walk for the cat" or determine which tasks apply to which pets.

3. **Added setter methods to Task class: `set_task_type()`, `set_duration()`, `set_priority()`, `set_frequency()`**
   - Reason: The app requires users to "add/edit tasks" (from README). Setters allow users to modify task attributes after creation.

4. **Updated `schedule()` method signature to include `pets` parameter: `schedule(owner: Owner, pets: List[Pet])`**
   - Reason: The scheduler needs to know which pets' tasks to organize. This parameter tells it which tasks to consider for scheduling.

5. **Added `get_scheduled_tasks()` method to DailySchedule**
   - Reason: Allows retrieval of the generated schedule after `schedule()` is called. Useful for the Streamlit UI to display the plan.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)? Available time and sequential scheduling are considered first then tasks are ordered based on 4-tier priority system.
1) Tasks with preferred times first.
2) Earlier times first (9:00 < 15:00)
3) More frequent tasks firsts (daily < weekly)
4) Critical tasks first (priority 1 < 3)
And all priority-1 (critical) tasks must be scheduled, and schedule cannot be empty.

- How did you decide which constraints mattered most?
If the owner's availability doesn't match with task it is hard to do the task, and if there is a sequence block of time and owner is available, it is easy for owner to complete it all at once. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It guaranteed to fit high-priority tasks first but it might leave gaps and it might drop lower-priority tasks unnecessarily.
- Why is that tradeoff reasonable for this scenario?
Because this schedule put pet health first, it prioritize its feeding and medications and other essentials first, then it fits with pet owner's schedule. Also it is simple, if there is any changes to the schedule, owner can change it easily. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI for:
1. **Writing comprehensive tests** — AI generated 19 test functions covering sorting, recurrence, conflict detection, and edge cases. This saved time and ensured thorough coverage.
2. **Refactoring app.py** — AI helped convert the starter template into a full Streamlit app with proper UI components (st.table, st.warning, st.success).
3. **Debugging syntax errors** — AI caught type mismatches (e.g., float vs int in Streamlit inputs) quickly.
4. **Documentation** — AI helped organize FEATURES.md, TEST_COVERAGE.md, and updated the UML to match the implementation.

- What kinds of prompts or questions were most helpful?

Most helpful prompts were **specific and task-focused**:
- "Draft test functions for sorting correctness, recurrence logic, and conflict detection with these edge cases..."
- "Update app.py to use DailySchedule methods like sorting, filtering, and conflict warnings with Streamlit components"
- "What are the most important edge cases to test for a pet scheduler?"

**Bad prompts:** Vague requests like "Help me with the project" didn't produce useful results.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

When AI initially suggested using `pytest`, I verified that `unittest` was already available without extra dependencies. I kept both options in the README but tested with unittest first since it's built-in.

- How did you evaluate or verify what the AI suggested?

I ran syntax checks (`python -m py_compile`) and executed tests (`python -m unittest`) to verify suggestions actually worked. I also read through generated code before accepting it to ensure it matched my system design.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested 7 core behaviors with 21 tests:
1. **Sorting Correctness** (4 tests) — Tasks scheduled in time order, priority order, frequency order
2. **Recurrence Logic** (5 tests) — Daily/weekly tasks create next occurrences, properties preserved, chains work
3. **Conflict Detection** (6 tests) — Overlapping tasks flagged, same-pet conflicts noted, multi-task scenarios
4. **Task Filtering** (2 tests) — Filter by completion status and pet name independently and combined
5. **Schedule Validation** (2 tests) — Critical tasks checked, errors reported
6. **Edge Cases** (4 tests) — Overflow handling, zero hours, null values, exact fits

- Why were these tests important?

These tests ensure the **core promise** of PawPal+ works: a scheduler that respects owner time, prioritizes pet health (critical tasks), and doesn't crash on edge cases. Without these tests, we couldn't trust the system.

**b. Confidence**

- How confident are you that your scheduler works correctly?

**4/5 stars** — Core logic is solid and well-tested. All 21 tests pass. I'm confident in:
- ✓ Scheduling logic respects constraints
- ✓ Recurring tasks work correctly
- ✓ Conflicts are detected
- ✓ Edge cases handled (null values, overflow, zero hours)

Less confident about:
- ? Performance with 100+ tasks (not tested)
- ? Date boundaries (month rollovers, leap years)
- ? Concurrent operations

- What edge cases would you test next if you had more time?

1. **Performance** — Schedule 100+ tasks and measure time
2. **Date boundaries** — Tasks spanning month/year boundaries, leap years
3. **Integration** — Full workflow: create owner → add 10 tasks → schedule → detect conflicts → complete task → verify recurrence
4. **Concurrent updates** — Mark multiple tasks complete simultaneously
5. **Invalid inputs** — Negative priority, duration = 0, invalid frequencies

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the **Conflict Detection algorithm**. It's elegant and solves a real problem:
- Detects overlapping tasks (hour-level grouping)
- Identifies same-pet conflicts specifically (e.g., can't give medication + food at same time to same pet)
- Returns warnings instead of crashing (graceful failure)
- Simple O(n) implementation with clear logic

This feature makes the scheduler actually usable because the owner can see and manually resolve conflicts.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

1. **Time precision** — Currently uses hour-level slots (9:00, 10:00). Real schedules need 15-min or 30-min slots.
2. **Recurring task editing** — If owner modifies a task, should it affect future occurrences? Currently no mechanism for this.
3. **Multi-pet scheduling** — Current design assumes single pet per owner. Real owners have multiple pets with different schedules.
4. **Flexible constraints** — Owner might prefer "no tasks after 5 PM" or "max 2 tasks per day." Current scheduler is rigid.
5. **Visual timeline** — Streamlit UI shows a table. A Gantt chart or timeline view would be clearer.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

**Design before coding matters.** I spent time on the UML before writing code, and this paid off:
- Clear class responsibilities → easy to test in isolation
- Well-defined methods → AI could generate tests automatically
- Good separation of concerns → Streamlit UI is simple (just calls scheduler methods)

Also: **AI is a tool, not a replacement for judgment.** AI was great at generating code patterns and tests, but *I* had to verify correctness, catch type errors, and decide tradeoffs (e.g., single-pet vs multi-pet, hour-level vs minute-level scheduling). The design decisions were still human-driven.

