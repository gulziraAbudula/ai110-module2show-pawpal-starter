"""
Main script to demonstrate PawPal+ scheduling system.
"""

from pawpal_system import Owner, Pet, Task, DailySchedule


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

    # Create tasks for the pets
    task1 = Task(
        title="Morning Walk - Max",
        task_type="walk",
        frequency="daily",
        duration=30,
        priority=1,
        pet=dog
    )

    task2 = Task(
        title="Feeding - Max",
        task_type="feeding",
        frequency="twice_daily",
        duration=10,
        priority=1,
        pet=dog
    )

    task3 = Task(
        title="Play Time - Max",
        task_type="play",
        frequency="daily",
        duration=20,
        priority=2,
        pet=dog
    )

    task4 = Task(
        title="Feeding - Luna",
        task_type="feeding",
        frequency="twice_daily",
        duration=5,
        priority=1,
        pet=cat
    )

    task5 = Task(
        title="Enrichment - Luna",
        task_type="play",
        frequency="daily",
        duration=15,
        priority=3,
        pet=cat
    )

    # Create schedule and add tasks
    schedule = DailySchedule()
    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)
    schedule.add_task(task4)
    schedule.add_task(task5)

    print(f"Tasks to schedule: {len(schedule.tasks)}")
    for i, task in enumerate(schedule.tasks, 1):
        print(f"  {i}. {task.get_title()} ({task.get_duration()}min, priority {task.get_priority()})")
    print()

    # Generate schedule
    scheduled_plan = schedule.schedule(owner, [dog, cat])

    # Display schedule
    print("=" * 60)
    print("TODAY'S SCHEDULE")
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

    print("\n" + "=" * 60)

    # Mark a task as completed
    task1.mark_completed()
    print(f"\n✓ Marked '{task1.get_title()}' as completed")
    print(f"  Completion status: {task1.get_completion_status()}")


if __name__ == "__main__":
    main()
