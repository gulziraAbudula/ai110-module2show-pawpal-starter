"""
Unit tests for PawPal+ system.
"""

import unittest
from pawpal_system import Owner, Pet, Task, DailySchedule


class TestTaskCompletion(unittest.TestCase):
    """Test task completion status."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Alice", "alice@email.com", 4)
        self.pet = Pet("Buddy", 3, "Dog", self.owner)
        self.task = Task(
            title="Morning Walk",
            task_type="walk",
            frequency="daily",
            duration=30,
            priority=1,
            pet=self.pet
        )

    def test_mark_completed_changes_status(self):
        """Verify that mark_completed() changes task's completion status from False to True."""
        # Initial state: task is not completed
        self.assertFalse(self.task.get_completion_status())

        # Mark task as completed
        self.task.mark_completed()

        # Verify status changed to True
        self.assertTrue(self.task.get_completion_status())


class TestDailySchedule(unittest.TestCase):
    """Test daily schedule task management."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Bob", "bob@email.com", 3)
        self.pet = Pet("Max", 2, "Cat", self.owner)
        self.schedule = DailySchedule()

    def test_adding_task_increases_task_count(self):
        """Verify that adding a task to schedule increases task count."""
        # Initial state: no tasks in schedule
        self.assertEqual(len(self.schedule.tasks), 0)

        # Create and add first task
        task1 = Task(
            title="Feeding",
            task_type="feeding",
            frequency="daily",
            duration=10,
            priority=1,
            pet=self.pet
        )
        self.schedule.add_task(task1)

        # Verify task count is 1
        self.assertEqual(len(self.schedule.tasks), 1)

        # Create and add second task for same pet
        task2 = Task(
            title="Playtime",
            task_type="play",
            frequency="daily",
            duration=15,
            priority=2,
            pet=self.pet
        )
        self.schedule.add_task(task2)

        # Verify task count is 2
        self.assertEqual(len(self.schedule.tasks), 2)


class TestSortingCorrectness(unittest.TestCase):
    """Test task sorting by time, frequency, and priority."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Charlie", "charlie@email.com", 5)
        self.pet1 = Pet("Buddy", 3, "Dog", self.owner)
        self.pet2 = Pet("Whiskers", 2, "Cat", self.owner)
        self.schedule = DailySchedule()

    def test_tasks_sorted_by_scheduled_time(self):
        """Verify tasks are scheduled in chronological order by start time."""
        from datetime import time

        # Add tasks with specific times (out of order)
        task_10am = Task("Lunch", "feeding", "daily", 20, 2, time=time(10, 0), pet=self.pet1)
        task_9am = Task("Walk", "walk", "daily", 30, 1, time=time(9, 0), pet=self.pet1)
        task_11am = Task("Play", "play", "daily", 15, 3, time=time(11, 0), pet=self.pet1)

        self.schedule.add_task(task_10am)
        self.schedule.add_task(task_9am)
        self.schedule.add_task(task_11am)

        scheduled = self.schedule.schedule(self.owner, [self.pet1])
        scheduled_times = list(scheduled.values())

        # Verify times are in ascending order
        self.assertEqual(scheduled_times, sorted(scheduled_times))

    def test_priority_sorting_without_specific_time(self):
        """Verify tasks without specific times are sorted by priority."""
        # Higher priority (lower number = more critical) scheduled first
        task_p3 = Task("Play", "play", "daily", 15, 3, pet=self.pet1)
        task_p1 = Task("Medication", "medication", "daily", 10, 1, pet=self.pet1)
        task_p2 = Task("Feeding", "feeding", "daily", 20, 2, pet=self.pet1)

        self.schedule.add_task(task_p3)
        self.schedule.add_task(task_p1)
        self.schedule.add_task(task_p2)

        scheduled = self.schedule.schedule(self.owner, [self.pet1])
        priorities = [t.priority for t in scheduled.keys()]

        # Critical task (p1) should be first
        self.assertEqual(priorities[0], 1)

    def test_frequency_ordering_breaks_ties(self):
        """Verify frequency ordering when priority and time are equal."""
        # Daily > twice_daily > weekly when priority is same
        task_weekly = Task("Vet", "checkup", "weekly", 30, 2, pet=self.pet1)
        task_daily = Task("Feeding", "feeding", "daily", 20, 2, pet=self.pet1)
        task_twice = Task("Medication", "medication", "twice_daily", 10, 2, pet=self.pet1)

        self.schedule.add_task(task_weekly)
        self.schedule.add_task(task_daily)
        self.schedule.add_task(task_twice)

        scheduled = self.schedule.schedule(self.owner, [self.pet1])
        frequencies = [t.frequency for t in scheduled.keys()]

        # Daily (0) should come before twice_daily (0.5) should come before weekly (2)
        self.assertEqual(frequencies[0], "daily")

    def test_empty_schedule_returns_empty_dict(self):
        """Verify scheduling with no tasks returns empty dictionary."""
        scheduled = self.schedule.schedule(self.owner, [])
        self.assertEqual(scheduled, {})


class TestRecurrenceLogic(unittest.TestCase):
    """Test recurring task creation and management."""

    def setUp(self):
        """Set up test fixtures."""
        from datetime import date
        self.owner = Owner("Diana", "diana@email.com", 4)
        self.pet = Pet("Fluffy", 1, "Rabbit", self.owner)
        self.schedule = DailySchedule()
        self.today = date.today()

    def test_daily_task_creates_next_occurrence(self):
        """Verify marking daily task complete creates next task with due_date tomorrow."""
        from datetime import timedelta

        task = Task(
            title="Morning Feed",
            task_type="feeding",
            frequency="daily",
            duration=10,
            priority=1,
            pet=self.pet
        )
        self.schedule.add_task(task)

        # Mark task as complete
        next_task = self.schedule.mark_task_complete(task)

        # Verify original task is marked completed
        self.assertTrue(task.is_completed)

        # Verify new task was created
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.frequency, "daily")
        self.assertEqual(next_task.due_date, self.today + timedelta(days=1))
        self.assertFalse(next_task.is_completed)

    def test_weekly_task_creates_next_occurrence(self):
        """Verify marking weekly task complete creates next task with due_date next week."""
        from datetime import timedelta

        task = Task(
            title="Vet Checkup",
            task_type="checkup",
            frequency="weekly",
            duration=60,
            priority=1,
            pet=self.pet
        )
        self.schedule.add_task(task)

        next_task = self.schedule.mark_task_complete(task)

        # Verify new task has due_date 7 days later
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.due_date, self.today + timedelta(days=7))

    def test_non_recurring_task_no_next_occurrence(self):
        """Verify non-recurring tasks return None and don't create next task."""
        task = Task(
            title="One-time Grooming",
            task_type="grooming",
            frequency="once",
            duration=45,
            priority=2,
            pet=self.pet
        )
        self.schedule.add_task(task)

        next_task = self.schedule.mark_task_complete(task)

        # Verify no next task created
        self.assertIsNone(next_task)
        # Verify original task still marked as completed
        self.assertTrue(task.is_completed)

    def test_recurring_task_properties_preserved(self):
        """Verify next occurrence inherits all properties from original task."""
        from datetime import time

        task = Task(
            title="Evening Walk",
            task_type="walk",
            frequency="daily",
            duration=45,
            priority=2,
            time=time(18, 30),
            pet=self.pet
        )
        self.schedule.add_task(task)

        next_task = self.schedule.mark_task_complete(task)

        # Verify all properties match
        self.assertEqual(next_task.title, task.title)
        self.assertEqual(next_task.task_type, task.task_type)
        self.assertEqual(next_task.duration, task.duration)
        self.assertEqual(next_task.priority, task.priority)
        self.assertEqual(next_task.time, task.time)
        self.assertEqual(next_task.pet, task.pet)

    def test_multiple_task_completions_create_chain(self):
        """Verify completing recurring task multiple times creates chain."""
        task = Task("Daily Feed", "feeding", "daily", 15, 1, pet=self.pet)
        self.schedule.add_task(task)

        # Complete task 3 times - each creates next occurrence
        task1 = self.schedule.mark_task_complete(task)
        task2 = self.schedule.mark_task_complete(task1)
        task3 = self.schedule.mark_task_complete(task2)

        # Verify chain: original + 3 next occurrences = 4 tasks
        # Each completed task marks as completed before creating next
        self.assertTrue(task.is_completed)
        self.assertTrue(task1.is_completed)
        self.assertTrue(task2.is_completed)
        self.assertFalse(task3.is_completed)  # Only the last one is uncompleted
        self.assertEqual(len(self.schedule.tasks), 4)


class TestConflictDetection(unittest.TestCase):
    """Test scheduling conflict detection."""

    def setUp(self):
        """Set up test fixtures."""
        from datetime import time
        self.owner = Owner("Eve", "eve@email.com", 3)
        self.pet1 = Pet("Rex", 4, "Dog", self.owner)
        self.pet2 = Pet("Mittens", 2, "Cat", self.owner)
        self.schedule = DailySchedule()

    def test_duplicate_times_flagged_as_conflict(self):
        """Verify tasks scheduled at same time are flagged as conflicts."""
        # Manually create scheduled tasks (same hour)
        task1 = Task("Walk", "walk", "daily", 30, 1, pet=self.pet1)
        task2 = Task("Feeding", "feeding", "daily", 20, 1, pet=self.pet2)

        self.schedule.scheduled_tasks[task1] = 9  # 9:00 AM
        self.schedule.scheduled_tasks[task2] = 9  # 9:00 AM (conflict!)

        conflicts = self.schedule.detect_scheduling_conflicts()

        # Verify conflict detected
        self.assertEqual(len(conflicts), 1)
        self.assertIn("Time conflict at 9:00", conflicts[0])

    def test_same_pet_conflict_noted(self):
        """Verify conflicts for same pet get special [SAME PET] note."""
        task1 = Task("Walk", "walk", "daily", 30, 1, pet=self.pet1)
        task2 = Task("Medication", "medication", "daily", 15, 1, pet=self.pet1)

        self.schedule.scheduled_tasks[task1] = 10
        self.schedule.scheduled_tasks[task2] = 10  # Same hour, same pet

        conflicts = self.schedule.detect_scheduling_conflicts()

        # Verify SAME PET note appears
        self.assertTrue(any("[SAME PET: Rex]" in c for c in conflicts))

    def test_different_pets_no_same_pet_note(self):
        """Verify conflicts for different pets don't include [SAME PET]."""
        task1 = Task("Walk", "walk", "daily", 30, 1, pet=self.pet1)
        task2 = Task("Feeding", "feeding", "daily", 20, 1, pet=self.pet2)

        self.schedule.scheduled_tasks[task1] = 10
        self.schedule.scheduled_tasks[task2] = 10  # Same hour, different pets

        conflicts = self.schedule.detect_scheduling_conflicts()

        # Verify no SAME PET note
        self.assertEqual(len(conflicts), 1)
        self.assertNotIn("[SAME PET", conflicts[0])

    def test_no_conflicts_returns_empty_list(self):
        """Verify non-overlapping tasks return no conflicts."""
        task1 = Task("Walk", "walk", "daily", 30, 1, pet=self.pet1)
        task2 = Task("Feeding", "feeding", "daily", 20, 2, pet=self.pet2)

        self.schedule.scheduled_tasks[task1] = 9   # Different hours
        self.schedule.scheduled_tasks[task2] = 10

        conflicts = self.schedule.detect_scheduling_conflicts()

        self.assertEqual(conflicts, [])

    def test_empty_schedule_no_conflicts(self):
        """Verify empty schedule has no conflicts."""
        conflicts = self.schedule.detect_scheduling_conflicts()
        self.assertEqual(conflicts, [])

    def test_three_way_conflict_detected(self):
        """Verify three tasks at same time are all listed in conflict."""
        task1 = Task("Walk", "walk", "daily", 30, 1, pet=self.pet1)
        task2 = Task("Feeding", "feeding", "daily", 20, 2, pet=self.pet2)
        task3 = Task("Meds", "medication", "daily", 15, 1, pet=self.pet1)

        self.schedule.scheduled_tasks[task1] = 9
        self.schedule.scheduled_tasks[task2] = 9
        self.schedule.scheduled_tasks[task3] = 9

        conflicts = self.schedule.detect_scheduling_conflicts()

        # Verify all three tasks mentioned in conflict
        conflict_msg = conflicts[0]
        self.assertIn("Walk", conflict_msg)
        self.assertIn("Feeding", conflict_msg)
        self.assertIn("Meds", conflict_msg)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def setUp(self):
        """Set up test fixtures."""
        self.owner = Owner("Frank", "frank@email.com", 2)
        self.pet = Pet("Spot", 5, "Dog", self.owner)
        self.schedule = DailySchedule()

    def test_tasks_overflow_available_hours(self):
        """Verify tasks exceeding owner hours are not all scheduled."""
        # Owner has 2 hours = 120 minutes
        task1 = Task("Long Walk", "walk", "daily", 90, 1, pet=self.pet)
        task2 = Task("Training", "training", "daily", 60, 2, pet=self.pet)

        self.schedule.add_task(task1)
        self.schedule.add_task(task2)

        scheduled = self.schedule.schedule(self.owner, [self.pet])

        # Only task1 should fit (90 min < 120 min)
        # task2 would exceed available hours
        self.assertIn(task1, scheduled)
        # task2 should not be scheduled (90 + 60 > 120)
        self.assertNotIn(task2, scheduled)

    def test_exact_fit_with_available_hours(self):
        """Verify tasks exactly matching available hours are scheduled."""
        # Owner has 2 hours = 120 minutes
        task1 = Task("Walk", "walk", "daily", 60, 1, pet=self.pet)
        task2 = Task("Play", "play", "daily", 60, 2, pet=self.pet)

        self.schedule.add_task(task1)
        self.schedule.add_task(task2)

        scheduled = self.schedule.schedule(self.owner, [self.pet])

        # Both should fit exactly
        self.assertEqual(len(scheduled), 2)

    def test_zero_available_hours(self):
        """Verify owner with zero hours has empty schedule."""
        no_time_owner = Owner("Gene", "gene@email.com", 0)
        task = Task("Walk", "walk", "daily", 30, 1, pet=self.pet)

        self.schedule.add_task(task)
        scheduled = self.schedule.schedule(no_time_owner, [self.pet])

        # Nothing should be scheduled
        self.assertEqual(len(scheduled), 0)

    def test_task_with_none_pet(self):
        """Verify task with pet=None doesn't crash conflict detection."""
        task1 = Task("Walk", "walk", "daily", 30, 1, pet=None)
        task2 = Task("Feeding", "feeding", "daily", 20, 1, pet=self.pet)

        self.schedule.scheduled_tasks[task1] = 9
        self.schedule.scheduled_tasks[task2] = 9

        conflicts = self.schedule.detect_scheduling_conflicts()

        # Should detect conflict and use "unknown pet"
        self.assertEqual(len(conflicts), 1)
        self.assertIn("unknown pet", conflicts[0])


if __name__ == "__main__":
    unittest.main()
