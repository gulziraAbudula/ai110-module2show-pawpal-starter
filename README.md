# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling Features

The scheduler includes several intelligent features to optimize pet care planning:

### **Multi-Tier Sorting**
Tasks are prioritized by:
1. **Preferred time** — Tasks scheduled for specific times (e.g., 9:00 AM walk) come first
2. **Task frequency** — Daily tasks before weekly tasks
3. **Priority level** — Critical tasks (priority 1) scheduled before lower priorities
4. **Availability** — Only tasks that fit within owner's available hours are scheduled

### **Recurring Task Management**
- When a **daily** or **weekly** task is marked complete, a new instance is automatically created for the next occurrence
- Due dates calculated with Python's `timedelta` (daily: today+1, weekly: today+7)
- Twice-daily tasks don't auto-recreate (they recur within the same day)

### **Task Filtering**
Filter tasks by:
- **Completion status** — View completed vs. incomplete tasks
- **Pet name** — See all tasks for a specific pet
- **Combined filters** — Find incomplete tasks for Max, completed tasks for Luna, etc.

### **Conflict Detection**
- Detects when multiple tasks are scheduled at the same time
- Identifies when the same pet has conflicting tasks (flagged as `[SAME PET: X]`)
- Returns warnings instead of crashing, allowing owners to manually resolve conflicts
- Uses lightweight O(n) algorithm with `defaultdict` for efficiency

### **Constraint-Based Optimization**
Hard constraints: Owner's available time, sequential scheduling starting at 9:00 AM
Soft constraints: Task preferences, frequency, priority
Tradeoff: Guarantees critical tasks fit, but may skip lower-priority tasks if time is tight (reasonable for pet health)

