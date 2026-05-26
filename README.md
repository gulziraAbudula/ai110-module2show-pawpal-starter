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

### Demo
<img src='/demo1.png' title='UI img' width='' alt='image' />
<img src='/demo2.png' title='UI img' width='' alt='image' />

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

## Features

PawPal+ implements 7 core scheduling algorithms optimized for pet care planning:

✅ **Multi-Tier Sorting** — Sort by preferred time → frequency → priority  
✅ **Constraint-Based Scheduling** — Respects owner availability, sequential placement  
✅ **Conflict Detection** — Flags overlapping times and same-pet conflicts  
✅ **Schedule Validation** — Ensures critical tasks are included  
✅ **Recurring Tasks** — Auto-creates daily/weekly next occurrences  
✅ **Task Filtering** — Filter by completion status and/or pet  
✅ **Schedule Explanation** — Human-readable plan output  

For algorithm details, complexity analysis, and examples, see **[FEATURES.md](FEATURES.md)**.

## Testing PawPal+

### Running Tests

```bash
# Using unittest (no additional dependencies)
python -m unittest tests.test_pawpal -v

# Or using pytest (if installed)
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite includes **21 comprehensive tests** across 6 test classes:

- **Sorting Correctness (4 tests)** — Verify tasks scheduled in chronological order, sorted by time/frequency/priority
- **Recurrence Logic (5 tests)** — Confirm daily and weekly tasks create next occurrences with correct due dates, properties preserved
- **Conflict Detection (6 tests)** — Verify scheduler flags duplicate times, detects same-pet conflicts, handles multi-task overlaps
- **Task Filtering (2 tests)** — Completion status and pet-name filtering work independently and combined
- **Schedule Validation (2 tests)** — Critical tasks checked, empty schedule detected
- **Edge Cases (4 tests)** — Overflow handling, exact-fit scheduling, zero hours, null pet references

**All tests passing:** ✅ 21/21 (100%)

For detailed coverage information, see [TEST_COVERAGE.md](TEST_COVERAGE.md).

### Confidence Level

**⭐⭐⭐⭐ (4/5 stars)**

**Strengths:**
- Core scheduling logic well-tested and reliable
- Edge cases covered (overflow, boundary conditions, null values)
- Recurrence chains work correctly across multiple completions
- Conflict detection accurate for single and multi-task scenarios
- 100% test pass rate with comprehensive assertions

**Areas for Future Improvement:**
- Performance tests with 100+ tasks
- Date boundary tests (month/year rollovers, leap years)
- Integration tests for full workflow (schedule → conflict → complete → recurrence)
- Concurrent task operations

