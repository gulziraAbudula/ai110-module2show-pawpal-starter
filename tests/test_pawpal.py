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


if __name__ == "__main__":
    unittest.main()
