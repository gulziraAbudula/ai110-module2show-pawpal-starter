# PawPal+ Features

## Core Scheduling Features

### 1. Multi-Tier Task Sorting
**Algorithm:** Lexicographic sort with 4-level priority key

Tasks are sorted in the following order:
1. **Preferred Time** — Tasks with specific times (e.g., 9:00 AM walk) scheduled first
2. **Actual Time Value** — Earlier times scheduled before later times  
3. **Frequency Weighting** — Daily (0) > Twice-daily (0.5) > Weekly (2)
4. **Priority Level** — Critical (1) > High (2) > Medium (3) > Low (4) > Optional (5)

**When used:** Every time `schedule()` is called to arrange tasks for the day

**Example:**
```
Task A: 9:00 AM walk (daily, priority 1) → First
Task B: No time, feeding (daily, priority 1) → Second  
Task C: 2:00 PM play (weekly, priority 3) → Third
Task D: No time, checkup (weekly, priority 5) → Last
```

---

### 2. Constraint-Based Scheduling
**Algorithm:** Sequential scheduling with capacity checking

Respects hard constraints to ensure feasibility:
- **Owner availability** — Only schedules tasks that fit within owner's available hours
- **Sequential placement** — Tasks placed starting at 9:00 AM, advancing by task duration
- **Overflow handling** — Lower-priority tasks dropped if exceeding available time

**When used:** During `schedule()` to build the daily timetable

**Example:**
- Owner has 2 hours (120 minutes) available
- Task 1: 60 min ✓ (fits, starts at 9:00 AM)
- Task 2: 60 min ✓ (fits, starts at 10:00 AM)
- Task 3: 45 min ✗ (skipped, would exceed 120 min)

---

### 3. Conflict Detection & Warnings
**Algorithm:** Hour-level grouping with multi-level flagging

Detects when multiple tasks are scheduled at overlapping times:
- **Grouping** — Tasks grouped by integer hour (9:00, 10:00, 11:00, etc.)
- **Overlap detection** — Flags when 2+ tasks share same hour
- **Same-pet flagging** — Adds `[SAME PET: Name]` note for conflicts involving same pet
- **Non-fatal** — Returns warnings instead of rejecting schedule (owner can manually resolve)

**When used:** `detect_scheduling_conflicts()` to identify scheduling problems

**Example:**
```
9:00 AM: Walk (Rex) + Medication (Rex)
⚠ Time conflict at 9:00: 'Walk' (Rex), 'Medication' (Rex) [SAME PET: Rex]

10:00 AM: Feeding (Luna) + Training (Max)
⚠ Time conflict at 10:00: 'Feeding' (Luna), 'Training' (Max)
```

---

### 4. Schedule Validation
**Algorithm:** Predicate checking on critical tasks

Validates schedule meets minimum requirements:
- **Critical task guarantee** — All priority 1 (critical) tasks must be scheduled
- **Completeness check** — Fails if no tasks scheduled at all
- **Error reporting** — Returns human-readable error messages

**When used:** `validate()` called before presenting schedule to user

**Example:**
```
Critical tasks: Medication (P1), Feeding (P1)
Scheduled tasks: Medication (P1), Play (P3)
Result: ✗ INVALID - "Not all critical tasks (priority 1) are scheduled"
```

---

### 5. Recurring Task Management
**Algorithm:** Property inheritance with timedelta-based recurrence

Automatically creates next occurrence when task marked complete:

**Daily recurrence:**
- Creates new task with `due_date = today + 1 day`
- Inherits all properties (title, duration, priority, pet, time)
- Original task marked as `is_completed = True`

**Weekly recurrence:**
- Creates new task with `due_date = today + 7 days`
- Preserves all other properties identically

**Non-recurring tasks:**
- Returns `None` (no next occurrence created)
- Only original task marked complete

**When used:** `mark_task_complete()` for task lifecycle management

**Example:**
```
Original Task: "Morning Feed" (daily, priority 1)
After completion:
  → Original marked as completed
  → Next task created with due_date = 2026-05-27

After 3 completions:
  → Chain: Task 1 (done) → Task 2 (done) → Task 3 (done) → Task 4 (pending)
```

---

### 6. Task Filtering
**Algorithm:** Dual-predicate filtering with AND logic

Filters tasks by one or more criteria:
- **By completion status** — View only completed tasks, incomplete tasks, or all
- **By pet name** — View tasks for specific pet only
- **Combined filtering** — Both predicates applied (AND operation)

**When used:** `filter_tasks()` to find tasks matching user criteria

**Example:**
```
All tasks: [Feed Luna, Walk Rex, Feed Rex, Groom Luna, Walk Luna]

Filter: incomplete + pet="Rex"
Result: [Walk Rex, Feed Rex]

Filter: completed + pet="Luna"
Result: [Groom Luna]
```

---

### 7. Schedule Explanation
**Algorithm:** Template-based formatted output

Generates human-readable schedule summary:
- **Time formatting** — Converts decimal hours to HH:MM format (9.5 → 09:30)
- **Task details** — Shows title, duration, priority for each slot
- **Chronological order** — Tasks sorted by start time

**When used:** `explain()` to display schedule to user

**Example Output:**
```
Schedule:
  09:00 - Morning Walk (30min, priority 1)
  09:30 - Feeding (20min, priority 1)
  10:00 - Playtime (15min, priority 2)
```

---

## Algorithm Complexity

| Feature | Time | Space | Notes |
|---------|------|-------|-------|
| Multi-tier Sorting | O(n log n) | O(n) | Standard comparison sort |
| Constraint Scheduling | O(n) | O(n) | Single pass with O(1) checks |
| Conflict Detection | O(n) | O(n) | Hash grouping by hour |
| Schedule Validation | O(n) | O(1) | Predicate checking |
| Recurring Tasks | O(1) | O(1) | Property inheritance only |
| Task Filtering | O(n) | O(n) | Linear scan with predicates |
| Schedule Explanation | O(n log n) | O(n) | Sorting + string formatting |

---

## Data Flow

```
Owner + Pet Inputs
        ↓
Add Tasks to DailySchedule
        ↓
schedule(owner, pets) 
    ├─ Sort tasks (multi-tier)
    ├─ Fit within constraints
    └─ Generate scheduled_tasks dict
        ↓
detect_scheduling_conflicts()
    └─ Group by hour, flag overlaps
        ↓
validate()
    └─ Check critical tasks included
        ↓
Display + Mark Complete
    └─ mark_task_complete() → creates next occurrence
        ↓
filter_tasks() for user queries
```

---

## Edge Cases Handled

✅ **Tasks with no preferred time** — Placed after time-specific tasks  
✅ **Zero owner available hours** — Returns empty schedule  
✅ **Tasks exceeding total hours** — Lower-priority tasks skipped  
✅ **Null pet references** — Uses "unknown pet" in conflict warnings  
✅ **Multiple tasks same hour** — All listed in conflict warning  
✅ **Recurring task chains** — Seamlessly creates multiple next occurrences  
✅ **Non-recurring tasks** — Returns None, no infinite loop  

---

## Integration with Streamlit UI

- **Sort display** — Schedule shown in sorted, time-ordered table
- **Conflict warnings** — `st.warning()` for each detected conflict
- **Validation status** — `st.success()` / `st.warning()` based on validate()
- **Filter UI** — Dropdown selectors call `filter_tasks()` with predicates
- **Task completion** — "Done" button calls `mark_task_complete()` and reloads
- **Explanation** — `st.code()` displays output of `explain()`
