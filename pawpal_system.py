"""
PawPal+ System: Classes for managing pet care scheduling.

This module provides dataclasses and logic for representing pets, owners, tasks,
and daily schedules for pet care planning.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import time, date, timedelta
from collections import defaultdict


@dataclass
class Owner:
    """Represents a pet owner."""
    name: str
    email: str
    available_hours: int

    def get_name(self) -> str:
        """Return the owner's name."""
        return self.name

    def set_name(self, name: str) -> None:
        """Set the owner's name."""
        self.name = name

    def get_email(self) -> str:
        """Return the owner's email."""
        return self.email

    def set_email(self, email: str) -> None:
        """Set the owner's email."""
        self.email = email

    def get_available_hours(self) -> int:
        """Return available hours per day for pet care."""
        return self.available_hours

    def set_available_hours(self, hours: int) -> None:
        """Set available hours per day for pet care."""
        self.available_hours = hours


@dataclass
class Pet:
    """Represents a pet."""
    name: str
    age: int
    breed: str
    owner: 'Owner' = None

    def get_name(self) -> str:
        """Return the pet's name."""
        return self.name

    def set_name(self, name: str) -> None:
        """Set the pet's name."""
        self.name = name

    def get_age(self) -> int:
        """Return the pet's age in years."""
        return self.age

    def set_age(self, age: int) -> None:
        """Set the pet's age in years."""
        self.age = age

    def get_breed(self) -> str:
        """Return the pet's breed."""
        return self.breed

    def set_breed(self, breed: str) -> None:
        """Set the pet's breed."""
        self.breed = breed


@dataclass
class Task:
    """Represents a pet care task."""
    title: str
    task_type: str
    frequency: str
    duration: int
    priority: int
    time: Optional[time] = None
    due_date: Optional[date] = None
    is_completed: bool = False
    pet: 'Pet' = None

    def __hash__(self):
        """Make Task hashable for use as dictionary keys."""
        return hash(id(self))

    def get_title(self) -> str:
        """Return the task title."""
        return self.title

    def set_title(self, title: str) -> None:
        """Set the task title."""
        self.title = title

    def get_task_type(self) -> str:
        """Return the task type (walk, feeding, medication, etc.)."""
        return self.task_type

    def set_task_type(self, task_type: str) -> None:
        """Set the task type."""
        self.task_type = task_type

    def get_duration(self) -> int:
        """Return the task duration in minutes."""
        return self.duration

    def set_duration(self, duration: int) -> None:
        """Set the task duration in minutes."""
        self.duration = duration

    def get_priority(self) -> int:
        """Return the task priority (1-5, where 1 is critical)."""
        return self.priority

    def set_priority(self, priority: int) -> None:
        """Set the task priority (1-5, where 1 is critical)."""
        self.priority = priority

    def get_frequency(self) -> str:
        """Return the task frequency (daily, twice_daily, weekly)."""
        return self.frequency

    def set_frequency(self, frequency: str) -> None:
        """Set the task frequency (daily, twice_daily, weekly)."""
        self.frequency = frequency

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def get_completion_status(self) -> bool:
        """Return whether this task is completed."""
        return self.is_completed


@dataclass
class DailySchedule:
    """Represents a daily schedule for pet care tasks."""
    tasks: List[Task] = field(default_factory=list)
    scheduled_tasks: Dict[Task, int] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def schedule(self, owner: Owner, pets: List[Pet]) -> Dict[Task, int]:
        """Arrange tasks in a schedule based on owner constraints and task priorities."""
        self.scheduled_tasks = {}

        if not self.tasks:
            return self.scheduled_tasks

        frequency_order = {"daily": 0, "twice_daily": 0.5, "weekly": 2}
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (t.time is None, t.time, frequency_order.get(t.frequency, 1), t.priority)
        )

        current_hour = 9
        available_minutes = owner.available_hours * 60
        used_minutes = 0

        for task in sorted_tasks:
            if used_minutes + task.duration <= available_minutes:
                self.scheduled_tasks[task] = current_hour
                used_minutes += task.duration
                current_hour += task.duration / 60

        return self.scheduled_tasks

    def validate(self) -> bool:
        """Check if the schedule is valid (no overlaps, fits available hours, critical tasks included)."""
        return len(self.get_validation_errors()) == 0

    def get_validation_errors(self) -> List[str]:
        """Return a list of validation errors if any."""
        errors = []

        if not self.scheduled_tasks:
            errors.append("No tasks scheduled")
            return errors

        critical_tasks = [t for t in self.tasks if t.priority == 1]
        scheduled_critical = [t for t in self.scheduled_tasks if t.priority == 1]

        if len(scheduled_critical) < len(critical_tasks):
            errors.append("Not all critical tasks (priority 1) are scheduled")

        return errors

    def explain(self) -> str:
        """Generate a human-readable explanation of the schedule."""
        if not self.scheduled_tasks:
            return "No tasks scheduled."

        explanation = "Schedule:\n"
        for task, hour in sorted(self.scheduled_tasks.items(), key=lambda x: x[1]):
            hour_str = f"{int(hour)}:00" if hour == int(hour) else f"{int(hour)}:{int((hour % 1) * 60):02d}"
            explanation += f"  {hour_str} - {task.title} ({task.duration}min, priority {task.priority})\n"

        return explanation

    def get_scheduled_tasks(self) -> Dict[Task, int]:
        """Retrieve the generated schedule."""
        return self.scheduled_tasks

    def filter_tasks(self, is_completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.

        Args:
            is_completed: True for completed tasks, False for incomplete, None to ignore completion status
            pet_name: Filter by pet name, None to include all pets

        Returns:
            List of tasks matching the filter criteria
        """
        filtered = self.tasks

        if is_completed is not None:
            filtered = [t for t in filtered if t.is_completed == is_completed]

        if pet_name is not None:
            filtered = [t for t in filtered if t.pet and t.pet.name == pet_name]

        return filtered

    def detect_scheduling_conflicts(self) -> List[str]:
        """Detect tasks scheduled at overlapping times and return warnings.

        Lightweight conflict detection that checks if multiple tasks are scheduled
        at the same time. Returns warnings rather than raising exceptions.

        Returns:
            List of warning messages for any detected conflicts
        """
        warnings = []

        if not self.scheduled_tasks:
            return warnings

        # Group tasks by start time
        time_groups = {}
        for task, hour in self.scheduled_tasks.items():
            hour_key = int(hour)  # Round to nearest hour for grouping
            if hour_key not in time_groups:
                time_groups[hour_key] = []
            time_groups[hour_key].append(task)

        # Check for conflicts
        for hour, tasks_at_hour in time_groups.items():
            if len(tasks_at_hour) > 1:
                task_info = []
                pet_names = []
                for task in tasks_at_hour:
                    pet_name = task.pet.name if task.pet else "unknown pet"
                    task_info.append(f"'{task.title}' ({pet_name})")
                    pet_names.append(pet_name)

                hour_str = f"{hour}:00"
                warning = f"⚠ Time conflict at {hour_str}: {', '.join(task_info)}"

                # Add note if same pet
                if len(set(pet_names)) == 1:
                    warning += f" [SAME PET: {pet_names[0]}]"

                warnings.append(warning)

        return warnings

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark a task as complete and create next occurrence if recurring.

        For daily and weekly tasks, automatically creates a new instance for the next occurrence
        with due_date calculated using timedelta (daily: today+1, weekly: today+7).

        Args:
            task: The task to mark as complete

        Returns:
            The new task instance if recurring, None if not recurring
        """
        task.mark_completed()

        if task.frequency in ("daily", "weekly"):
            today = date.today()
            if task.frequency == "daily":
                next_due_date = today + timedelta(days=1)
            else:  # weekly
                next_due_date = today + timedelta(days=7)

            next_task = Task(
                title=task.title,
                task_type=task.task_type,
                frequency=task.frequency,
                duration=task.duration,
                priority=task.priority,
                time=task.time,
                due_date=next_due_date,
                is_completed=False,
                pet=task.pet
            )
            self.add_task(next_task)
            return next_task

        return None
