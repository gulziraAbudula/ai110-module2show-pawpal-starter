"""
Main script to demonstrate PawPal+ scheduling system.
"""

from pawpal_system import Owner, Pet, Task, DailySchedule
from datetime import time, date


def main():
    # Create an owner
    owner = Owner(
        name="Sarah",
        email="sarah@email.com",
        available_hours=4
    )

    print("=" * 60)
    print(f"PawPal+ Daily Schedule for {owner.get_name()}")
    print("=" * 60)
    print(f"Available time: {owner.get_available_hours()} hours\n")

    # Create pets
    dog = Pet(
        name="Max",
        age=3,
        breed="Golden Retriever",
        owner=owner
    )

    cat = Pet(
        name="Luna",
        age=2,
        breed="Siamese",
        owner=owner
    )

    print(f"Pets: {dog.get_name()} ({dog.get_breed()}) and {cat.get_name()} ({cat.get_breed()})\n")

    # Create tasks OUT OF ORDER with different times and priorities
    task1 = Task(
        title="Morning Walk - Max",
        task_type="walk",
        frequency="daily",
        duration=30,
        priority=1,
        time=time(9, 0),
        due_date=date.today(),
        pet=dog
    )

    task2 = Task(
        title="Feeding - Max",
        task_type="feeding",
        frequency="twice_daily",
        duration=10,
        priority=1,
        due_date=date.today(),
        pet=dog
    )

    task3 = Task(
        title="Play Time - Max",
        task_type="play",
        frequency="daily",
        duration=20,
        priority=2,
        time=time(15, 0),
        due_date=date.today(),
        pet=dog
    )

    task4 = Task(
        title="Feeding - Luna",
        task_type="feeding",
        frequency="twice_daily",
        duration=5,
        priority=1,
        time=time(12, 0),
        due_date=date.today(),
        pet=cat
    )

    task5 = Task(
        title="Enrichment - Luna",
        task_type="play",
        frequency="daily",
        duration=15,
        priority=3,
        due_date=date.today(),
        pet=cat
    )

    # Create a conflicting task (same time as Morning Walk)
    task6 = Task(
        title="Vet Appointment - Max",
        task_type="medical",
        frequency="weekly",
        duration=45,
        priority=1,
        time=time(9, 0),
        due_date=date.today(),
        pet=dog
    )

    # Add tasks OUT OF ORDER: 2, 5, 1, 4, 3, 6
    schedule = DailySchedule()
    schedule.add_task(task2)
    schedule.add_task(task5)
    schedule.add_task(task1)
    schedule.add_task(task4)
    schedule.add_task(task3)
    schedule.add_task(task6)

    print("=" * 60)
    print("TASKS ADDED (OUT OF ORDER)")
    print("=" * 60)
    for i, task in enumerate(schedule.tasks, 1):
        time_str = f"@ {task.time.strftime('%H:%M')}" if task.time else "@ flexible"
        due_str = f"(due: {task.due_date})" if task.due_date else "(no due date)"
        print(f"  {i}. {task.get_title()} ({task.get_duration()}min, priority {task.get_priority()}) {time_str} {due_str}")
    print()

    # Generate schedule (uses new sorting logic)
    scheduled_plan = schedule.schedule(owner, [dog, cat])

    # Display schedule
    print("=" * 60)
    print("TODAY'S SCHEDULE (SORTED)")
    print("=" * 60)
    print(schedule.explain())

    # Validate schedule
    print("=" * 60)
    print("VALIDATION")
    print("=" * 60)
    is_valid = schedule.validate()
    if is_valid:
        print("✓ Schedule is valid")
    else:
        print("✗ Schedule has issues:")
        for error in schedule.get_validation_errors():
            print(f"  - {error}")

    # Detect scheduling conflicts
    print("\n" + "=" * 60)
    print("CONFLICT DETECTION")
    print("=" * 60)
    conflicts = schedule.detect_scheduling_conflicts()
    if conflicts:
        print("⚠ Scheduling conflicts detected:")
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("✓ No scheduling conflicts detected")

    # Mark some tasks as completed (with recurring task creation)
    print("\n" + "=" * 60)
    print("COMPLETING TASKS (RECURRING TASKS AUTOMATICALLY RECREATED)")
    print("=" * 60)

    next_task1 = schedule.mark_task_complete(task1)
    print(f"\n✓ Marked '{task1.get_title()}' as completed")
    if next_task1:
        print(f"  → New recurring task created: '{next_task1.get_title()}'")
        print(f"  → Due date: {next_task1.due_date} (today + 1 day via timedelta)")

    next_task4 = schedule.mark_task_complete(task4)
    print(f"✓ Marked '{task4.get_title()}' as completed")
    if next_task4:
        print(f"  → No new task created (twice_daily is not daily/weekly)")

    next_task5 = schedule.mark_task_complete(task5)
    print(f"✓ Marked '{task5.get_title()}' as completed")
    if next_task5:
        print(f"  → New recurring task created: '{next_task5.get_title()}'")
        print(f"  → Due date: {next_task5.due_date} (today + 1 day via timedelta)")

    print(f"\nTotal tasks now in schedule: {len(schedule.tasks)}")

    # Filter and display results
    print("\n" + "=" * 60)
    print("FILTERING EXAMPLES")
    print("=" * 60)

    completed_tasks = schedule.filter_tasks(is_completed=True)
    print(f"\n✓ Completed tasks ({len(completed_tasks)}):")
    for task in completed_tasks:
        print(f"  - {task.get_title()}")

    incomplete_tasks = schedule.filter_tasks(is_completed=False)
    print(f"\n✗ Incomplete tasks ({len(incomplete_tasks)}):")
    for task in incomplete_tasks:
        print(f"  - {task.get_title()}")

    # Filter tasks by pet name
    max_tasks = schedule.filter_tasks(pet_name="Max")
    print(f"\n🐕 Tasks for Max ({len(max_tasks)}):")
    for task in max_tasks:
        status = "✓ done" if task.is_completed else "✗ pending"
        print(f"  - {task.get_title()} [{status}]")

    luna_tasks = schedule.filter_tasks(pet_name="Luna")
    print(f"\n🐱 Tasks for Luna ({len(luna_tasks)}):")
    for task in luna_tasks:
        status = "✓ done" if task.is_completed else "✗ pending"
        print(f"  - {task.get_title()} [{status}]")

    # Combine filters: incomplete tasks for Max
    max_incomplete = schedule.filter_tasks(is_completed=False, pet_name="Max")
    print(f"\n⏳ Incomplete tasks for Max ({len(max_incomplete)}):")
    for task in max_incomplete:
        print(f"  - {task.get_title()}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
