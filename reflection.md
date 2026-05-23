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
    =======
    __init__(name, age, breed)
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
    =======
    __init__(title, task_type, frequency, duration, priority)
    get_title() -> str
    set_title(title: str)
    get_task_type() -> str
    get_duration() -> int
    get_priority() -> int
    get_frequency() -> str
    mark_completed() — Set is_completed = True
    get_completion_status() -> bool
daily schedule:
    tasks: list[Task] — All tasks to schedule
    scheduled_tasks: dict — Format: {task: start_hour} (e.g., {walk_task: 9} means 9am)
    =======
    __init__(tasks)
    schedule(owner: Owner) -> dict — Arrange tasks, return {task: start_hour}. Prioritizes by frequency + priority
    validate() -> bool — Check: no overlaps, total duration fits available hours, critical tasks included
    get_validation_errors() -> list[str] — Return list of problems (if any)
    explain() -> str — Simple explanation: "Task X at 9am because it's priority 1" format


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
