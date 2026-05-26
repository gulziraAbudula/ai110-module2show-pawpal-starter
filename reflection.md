# PawPal+ Project Reflection

## 1. System Design

### Initial design

**Main behaviors:**
1. Enter basic owner and pet information
2. Add and edit tasks (duration + priority at minimum)
3. Generate a daily schedule/plan based on constraints and priorities
4. Display the plan clearly (and ideally explain the reasoning)
5. Include tests for the most important scheduling behaviors

**Class structure:**

| Class | Attributes | Key Methods |
|-------|-----------|------------|
| **Owner** | name, email, available_hours | get/set name, email, hours |
| **Pet** | name, age, breed, owner | get/set name, age, breed |
| **Task** | title, task_type, frequency, duration, priority, is_completed, pet | get/set properties, mark_completed() |
| **DailySchedule** | tasks, scheduled_tasks | schedule(), validate(), explain(), get_scheduled_tasks() |

### Design changes

**5 major changes during implementation:**

1. **Added `owner: Owner` to Pet class** — Each pet needs to know its owner for relationship tracking
2. **Added `pet: Pet` to Task class** — Critical to distinguish tasks between different pets
3. **Added setter methods to Task** — Required for "add/edit tasks" feature in the app
4. **Updated `schedule()` signature** — Added `pets` parameter so scheduler knows which pets to schedule for
5. **Added `get_scheduled_tasks()` method** — Allows Streamlit UI to retrieve and display the generated schedule

---

## 2. Scheduling Logic and Tradeoffs

### Constraints and priorities

**What the scheduler considers:**
- Available time (owner's hours per day)
- Sequential scheduling (starting at 9:00 AM)
- 4-tier priority system: preferred time → earlier times → frequency (daily < weekly) → priority (1 = critical)

**Why these constraints:** Owner availability is the hard constraint. Sequential blocks of time are easier for owners to follow than scattered tasks.

### Tradeoffs

**Tradeoff made:** Guarantees high-priority tasks fit first, but may drop lower-priority tasks or leave gaps.

**Why reasonable:** Pet health comes first (feeding, meds are critical). Owner can manually adjust if needed. Simple design is easy to understand and modify.

---

## 3. AI Collaboration

### How you used AI

**4 main uses:**
1. Writing 19 comprehensive test functions (sorting, recurrence, conflicts, edge cases)
2. Refactoring app.py into a full Streamlit app with proper UI components
3. Debugging syntax errors (e.g., type mismatches in Streamlit inputs)
4. Organizing documentation (FEATURES.md, TEST_COVERAGE.md, UML updates)

**Most helpful prompts:** Specific, task-focused requests like "Draft test functions for sorting correctness, recurrence logic, and conflict detection" worked best. Vague requests didn't.

### Judgment and verification

**Example of skepticism:** AI suggested using `pytest`, but I verified that `unittest` was built-in with no extra dependencies. Kept both options in README, tested with unittest first.

**How I verified:** Ran syntax checks and executed tests to verify suggestions worked. Read through generated code to ensure it matched my system design.

---

## 4. Testing and Verification

### What you tested

**7 core behaviors with 21 tests:**

| Behavior | Tests | Coverage |
|----------|-------|----------|
| Sorting Correctness | 4 | Time order, priority order, frequency order |
| Recurrence Logic | 5 | Daily/weekly, property inheritance, chains |
| Conflict Detection | 6 | Overlaps, same-pet conflicts, multi-task |
| Task Filtering | 2 | By status + pet, combined filtering |
| Schedule Validation | 2 | Critical tasks, error messages |
| Edge Cases | 4 | Overflow, zero hours, null values |

**Why important:** Verify the core promise of PawPal+ — respects owner time, prioritizes pet health, handles edge cases gracefully.

### Confidence

**Rating: ⭐⭐⭐⭐ (4/5 stars)**

**Confident in:**
- ✓ Scheduling logic respects constraints
- ✓ Recurring tasks work correctly
- ✓ Conflicts detected accurately
- ✓ Edge cases handled

**Less confident:**
- ? Performance with 100+ tasks
- ? Date boundaries (month/year rollovers)
- ? Concurrent operations

**Next tests to add:**
- Performance test with 100+ tasks
- Date boundary tests (month/year rollovers)
- Full integration test (create → schedule → complete → recurrence)
- Concurrent task updates
- Invalid input handling

---

## 5. Reflection

### What went well

**Most satisfied with:** Conflict Detection algorithm
- Elegantly detects overlapping tasks (hour-level grouping)
- Flags same-pet conflicts specifically
- Returns warnings instead of crashing (graceful degradation)
- Simple O(n) implementation

Makes the scheduler usable because owners can see and resolve conflicts manually.

### What you would improve

**5 improvements for next iteration:**

1. **Time precision** — Currently hour-level slots. Need 15-min or 30-min slots
2. **Recurring task editing** — Modifying a task should propagate to future occurrences
3. **Multi-pet scheduling** — Current design assumes single pet
4. **Flexible constraints** — "No tasks after 5 PM" or "max 2 tasks per day"
5. **Visual timeline** — Gantt chart or timeline view instead of just a table

### Key takeaway

**Design before coding matters.**
- Clear class responsibilities → easy to test in isolation
- Well-defined methods → AI could generate tests automatically
- Good separation of concerns → Streamlit UI is simple

**AI is a tool, not a replacement for judgment.**
- AI excelled at: generating code patterns, writing tests, catching syntax errors
- I handled: verification, catching type errors, deciding tradeoffs
- Design decisions were still human-driven
